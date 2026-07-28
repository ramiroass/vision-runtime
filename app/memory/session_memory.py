import time
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any

class FiveMinuteSessionMemory:
    def __init__(self, window_seconds: int = 300):
        self.window_seconds = window_seconds
        self.snapshots: List[Dict[str, Any]] = []

    def record_snapshot(self, scene: Dict[str, Any]):
        now = datetime.now(timezone.utc)
        snapshot = {
            "timestamp": now.isoformat(),
            "epoch": time.time(),
            "active_window": scene.get("active_window", "Desconocido"),
            "active_app": scene.get("active_app", "Desconocido"),
            "ocr_text": scene.get("ocr_text", ""),
            "buttons": scene.get("buttons", []),
            "confidence": scene.get("confidence", {}).get("overall", 0.90)
        }
        self.snapshots.append(snapshot)
        self._purge_old_snapshots()

    def _purge_old_snapshots(self):
        cutoff = time.time() - self.window_seconds
        self.snapshots = [s for s in self.snapshots if s["epoch"] >= cutoff]

    def get_history(self, seconds_ago: int = None) -> List[Dict[str, Any]]:
        self._purge_old_snapshots()
        if seconds_ago is None:
            return self.snapshots
        
        target_epoch = time.time() - seconds_ago
        # Retornar instantáneas más cercanas al tiempo solicitado
        return [s for s in self.snapshots if abs(s["epoch"] - target_epoch) <= 30]

five_minute_memory = FiveMinuteSessionMemory()
