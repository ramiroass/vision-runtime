import sqlite3
import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "events.db")

class EventsDatabase:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS intents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                intent_description TEXT NOT NULL,
                result_status TEXT NOT NULL,
                confidence REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def log_event(self, event_type: str, payload: Dict[str, Any]):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()
        cursor.execute(
            "INSERT INTO events (event_type, timestamp, payload_json) VALUES (?, ?, ?)",
            (event_type, now, json.dumps(payload))
        )
        conn.commit()
        conn.close()

    def log_intent(self, description: str, result_status: str = "OK", confidence: float = 0.95):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        now = datetime.now(timezone.utc).isoformat()
        cursor.execute(
            "INSERT INTO intents (timestamp, intent_description, result_status, confidence) VALUES (?, ?, ?, ?)",
            (now, description, result_status, confidence)
        )
        conn.commit()
        conn.close()

    def get_recent_intents(self, limit: int = 20) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, intent_description, result_status, confidence FROM intents ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "id": r[0],
                "timestamp": r[1],
                "description": r[2],
                "status": r[3],
                "confidence": r[4]
            }
            for r in rows
        ]

events_db = EventsDatabase()
