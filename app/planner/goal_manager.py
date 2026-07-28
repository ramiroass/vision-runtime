import time
from typing import Dict, Any, List, Optional

class GoalManager:
    def __init__(self):
        self.current_goal: Optional[Dict[str, Any]] = None
        self.goal_history: List[Dict[str, Any]] = []

    def set_long_term_goal(self, goal_title: str, description: str = "") -> Dict[str, Any]:
        """Establece un objetivo de largo plazo supervisado (Layer 6)."""
        goal = {
            "id": f"goal_{int(time.time())}",
            "title": goal_title,
            "description": description,
            "status": "ACTIVE",
            "created_at": time.time(),
            "subgoals": []
        }
        self.current_goal = goal
        self.goal_history.append(goal)
        return goal

    def get_current_goal_context(self) -> Dict[str, Any]:
        return self.current_goal or {"status": "IDLE", "title": "Sin objetivo activo"}

goal_manager = GoalManager()
