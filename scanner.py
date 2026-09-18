import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient, events

from database import init_db, save_message, save_ioc
from ioc_extractor import extract_iocs
from alerts import find_matches, send_alert_email

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE = os.getenv("TELEGRAM_PHONE")
CHANNELS = [c.strip() for c in os.getenv("CHANNELS_TO_WATCH", "").split(",") if c.strip()]

if not API_ID or not API_HASH:
    print("ERROR: Missing TELEGRAM_API_ID / TELEGRAM_API_HASH.")
    print("Copy .env.example to .env and fill in your credentials from https://my.telegram.org")
    exit(1)

if not CHANNELS:
    print("ERROR: No channels listed in CHANNELS_TO_WATCH in your .env file.")
    exit(1)

client = TelegramClient("scanner_session", API_ID, API_HASH)


def process_message(channel_name, message_id, text, sender_id, timestamp):
    db_id = save_message(channel_name, message_id, text, sender_id, timestamp)

    if db_id is None:
        return

    iocs = extract_iocs(text)
    for ioc_type, ioc_value in iocs:
        save_ioc(db_id, ioc_type, ioc_value)

    matches = find_matches(text)
    if matches:
        send_alert_email(channel_name, text, matches)

    preview = (text or "")[:60].replace("\n", " ")
    ioc_note = f" | {len(iocs)} IOC(s) found" if iocs else ""
    alert_note = f" | WATCH KEYWORD MATCH: {matches}" if matches else ""
    print(f"[{channel_name}] {preview}...{ioc_note}{alert_note}")


@client.on(events.NewMessage(chats=CHANNELS))
async def handle_new_message(event):
    process_message(
        channel_name=event.chat.username or str(event.chat_id),
        message_id=event.message.id,
        text=event.message.message,
        sender_id=event.message.sender_id,
        timestamp=datetime.utcnow().isoformat(),
    )


async def backfill_history(limit_per_channel=50):
    print(f"\nBackfilling last {limit_per_channel} messages per channel...\n")
    for channel in CHANNELS:
        try:
            async for message in client.iter_messages(channel, limit=limit_per_channel):
                if message.message:
                    process_message(
                        channel_name=channel,
                        message_id=message.id,
                        text=message.message,
                        sender_id=message.sender_id,
                        timestamp=message.date.isoformat(),
                    )
        except Exception as e:
            print(f"[warning] Could not backfill '{channel}': {e}")
    print("\nBackfill complete. Now watching for new messages live...\n")


async def main():
    init_db()
    await client.start(phone=PHONE)
    print("Logged into Telegram successfully.")
    await backfill_history()
    print("Scanner is running. Press Ctrl+C to stop.")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
