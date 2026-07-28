from typing import Callable, Dict, List, Any
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EventBus")

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
        self._event_history: List[Dict[str, Any]] = []

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, payload: Dict[str, Any]):
        event = {
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }
        self._event_history.append(event)
        if len(self._event_history) > 1000:
            self._event_history.pop(0)

        callbacks = self._subscribers.get(event_type, [])
        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error procesando callback en EventBus para {event_type}: {e}")

    def get_recent_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._event_history[-limit:]

event_bus = EventBus()
