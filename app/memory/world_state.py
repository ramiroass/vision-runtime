import time
from typing import Dict, Any, Optional

class WorldStateManager:
    def __init__(self):
        self.state: Dict[str, Any] = {
            "last_updated": time.time(),
            "active_window": "Windows Desktop",
            "active_app": "Windows Explorer",
            "current_file": None,
            "terminal": {"running": False, "last_exit_code": 0},
            "browser": {"url": "about:blank"},
            "mouse": {"x": 0, "y": 0},
            "confidence_score": 0.90
        }

    def update_from_scene(self, scene: Dict[str, Any]):
        """Actualiza el World State actual a partir del objeto Scene Description."""
        self.state["last_updated"] = time.time()
        self.state["active_window"] = scene.get("active_window", self.state["active_window"])
        self.state["active_app"] = scene.get("active_app", self.state["active_app"])
        self.state["confidence_score"] = scene.get("confidence", {}).get("overall", 0.90)

    def get_world_state(self) -> Dict[str, Any]:
        return self.state

world_state_manager = WorldStateManager()
