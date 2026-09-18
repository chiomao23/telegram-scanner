import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH", "scanner.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel TEXT NOT NULL,
            message_id INTEGER NOT NULL,
            text TEXT,
            sender_id INTEGER,
            timestamp TEXT NOT NULL,
            UNIQUE(channel, message_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iocs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_db_id INTEGER NOT NULL,
            ioc_type TEXT NOT NULL,
            ioc_value TEXT NOT NULL,
            FOREIGN KEY (message_db_id) REFERENCES messages (id)
        )
    """)

    conn.commit()
    conn.close()
    print(f"[database] Ready. Using file: {DB_PATH}")


def save_message(channel, message_id, text, sender_id, timestamp):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO messages (channel, message_id, text, sender_id, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (channel, message_id, text, sender_id, timestamp))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def save_ioc(message_db_id, ioc_type, ioc_value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO iocs (message_db_id, ioc_type, ioc_value)
        VALUES (?, ?, ?)
    """, (message_db_id, ioc_type, ioc_value))
    conn.commit()
    conn.close()


def search_messages(keyword):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM messages WHERE text LIKE ? ORDER BY timestamp DESC
    """, (f"%{keyword}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows


def search_iocs(ioc_type=None):
    conn = get_connection()
    cursor = conn.cursor()
    if ioc_type:
        cursor.execute("SELECT * FROM iocs WHERE ioc_type = ? ORDER BY id DESC", (ioc_type,))
    else:
        cursor.execute("SELECT * FROM iocs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
