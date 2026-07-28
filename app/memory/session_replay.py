import os
import json
from datetime import datetime, timezone
from typing import List, Dict, Any

REPLAY_CACHE_DIR = os.path.join(os.path.dirname(__file__), "sessions")

class SessionReplayEngine:
    def __init__(self):
        os.makedirs(REPLAY_CACHE_DIR, exist_ok=True)
        self.current_session_id = datetime.now().strftime("session_%Y%m%d_%H%M%S")
        self.session_file = os.path.join(REPLAY_CACHE_DIR, f"{self.current_session_id}.json")
        self.session_data: List[Dict[str, Any]] = []

    def record_step(self, frame_index: int, scene_data: Dict[str, Any], intent: str = None):
        step = {
            "frame_index": frame_index,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_window": scene_data.get("active_window", "Desconocido"),
            "ocr_text": scene_data.get("ocr_text", ""),
            "buttons": scene_data.get("buttons", []),
            "intent": intent,
            "confidence": scene_data.get("confidence", {}).get("overall", 0.90)
        }
        self.session_data.append(step)
        try:
            with open(self.session_file, "w", encoding="utf-8") as f:
                json.dump(self.session_data, f, indent=2)
        except Exception as e:
            print(f"Error grabando sesión de replay: {e}")

    def get_session_replay(self) -> Dict[str, Any]:
        return {
            "session_id": self.current_session_id,
            "total_frames_recorded": len(self.session_data),
            "timeline_steps": self.session_data[-50:]
        }

session_replay_engine = SessionReplayEngine()
