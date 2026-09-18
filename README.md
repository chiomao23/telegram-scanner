# Telegram IOC Scanner

A self-hosted tool for real-time Telegram channel monitoring with
automatic IOC (Indicator of Compromise) extraction, built as a
learning project to demonstrate threat intelligence collection skills.

## Features

- Real-time monitoring of chosen public Telegram channels
- Automatic extraction of IOCs (IP addresses, URLs, file hashes, emails)
  from every message, including "defanged" formats like hxxp:// and [.]
- Local SQLite database — no external server required
- Command-line search tool for collected data
- Optional personal-exposure email alerts: get notified if your own
  name, email, or phone number is ever mentioned in a watched channel

## How it works

1. `scanner.py` connects to Telegram using your own account credentials
2. It watches the channels you specify, saving every message
3. Each message is scanned for IOCs (`ioc_extractor.py`) and personal
   watch-keywords (`alerts.py`)
4. Everything is stored in a local SQLite database (`database.py`)
5. `search.py` lets you query what's been collected

## Setup

1. `pip install -r requirements.txt --break-system-packages`
2. Get Telegram API credentials from https://my.telegram.org
3. Copy `.env.example` to `.env` and fill in your details
4. Run `python3 scanner.py`

## Tech stack

Python, Telethon (Telegram MTProto client), SQLite, iocextract, smtplib

## Disclaimer

Built for educational/portfolio purposes. Only monitors public channels
using the account owner's own credentials. Does not access or store
illegally obtained data.
