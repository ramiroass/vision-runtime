import time
from typing import Dict, Any, List

class LearningEngine:
    def __init__(self):
        self.task_experiences: List[Dict[str, Any]] = []

    def record_experience(
        self,
        goal: str,
        plan: List[str],
        status: str,
        duration_seconds: float,
        errors: List[str] = None,
        correction_applied: str = None
    ) -> Dict[str, Any]:
        """Registra la experiencia de ejecución para optimizar estrategias futuras."""
        exp = {
            "timestamp": time.time(),
            "goal": goal,
            "plan": plan,
            "status": status,
            "duration_seconds": duration_seconds,
            "errors": errors or [],
            "correction_applied": correction_applied
        }
        self.task_experiences.append(exp)
        return exp

    def get_learnings_summary(self) -> Dict[str, Any]:
        total = len(self.task_experiences)
        successful = sum(1 for e in self.task_experiences if e["status"] == "SUCCESS")
        return {
            "total_experiences": total,
            "successful_experiences": successful,
            "success_rate": round(successful / total * 100, 1) if total > 0 else 100.0,
            "avg_duration_seconds": round(sum(e["duration_seconds"] for e in self.task_experiences) / total, 2) if total > 0 else 0.0
        }

learning_engine = LearningEngine()
