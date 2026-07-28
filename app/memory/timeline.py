import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Any
from app.event_bus import event_bus

TIMELINE_FILE = os.path.join(os.path.dirname(__file__), "timeline.jsonl")

class TimelineStreamLogger:
    def __init__(self):
        # Suscribirse al Event Bus para capturar todos los eventos
        event_bus.subscribe("FRAME_CAPTURED", self._on_event)
        event_bus.subscribe("SCENE_PROCESSED", self._on_event)

    def _on_event(self, event: Dict[str, Any]):
        try:
            with open(TIMELINE_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        except Exception as e:
            print(f"Error escribiendo en timeline stream: {e}")

    def get_recent_stream(self, limit: int = 50) -> List[Dict[str, Any]]:
        events = []
        if not os.path.exists(TIMELINE_FILE):
            return events
        try:
            with open(TIMELINE_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    events.append(json.loads(line.strip()))
        except Exception:
            pass
        return events

timeline_logger = TimelineStreamLogger()
