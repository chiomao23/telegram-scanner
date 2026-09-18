import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL = os.getenv("ALERT_FROM_EMAIL")
FROM_PASSWORD = os.getenv("ALERT_FROM_PASSWORD")
TO_EMAIL = os.getenv("ALERT_TO_EMAIL")

WATCH_KEYWORDS = [
    k.strip().lower()
    for k in os.getenv("WATCH_KEYWORDS", "").split(",")
    if k.strip()
]


def find_matches(text):
    if not text or not WATCH_KEYWORDS:
        return []

    text_lower = text.lower()
    return [kw for kw in WATCH_KEYWORDS if kw in text_lower]


def send_alert_email(channel_name, message_text, matched_keywords):
    if not FROM_EMAIL or not FROM_PASSWORD or not TO_EMAIL:
        print("[alerts] Email not configured — skipping alert.")
        return False

    subject = f"Watch keyword found in Telegram channel: {channel_name}"
    body = (
        f"One of your watched keywords was mentioned.\n\n"
        f"Channel: {channel_name}\n"
        f"Matched keyword(s): {', '.join(matched_keywords)}\n\n"
        f"Message:\n{message_text}\n"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(FROM_EMAIL, FROM_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        print(f"[alerts] Email sent — matched: {matched_keywords}")
        return True
    except Exception as e:
        print(f"[alerts] Failed to send email: {e}")
        return False


if __name__ == "__main__":
    print("Testing keyword matching...")
    print(f"WATCH_KEYWORDS loaded: {WATCH_KEYWORDS}")

    if not WATCH_KEYWORDS:
        print("No keywords set in .env — nothing to test.")
    else:
        test_text = f"This is a test message mentioning {WATCH_KEYWORDS[0]}."
        matches = find_matches(test_text)
        print(f"Matches found: {matches}")
        if matches:
            print("Attempting to send a real test email now...")
            send_alert_email("test-channel", test_text, matches)
