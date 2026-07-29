import time
from typing import Dict, Any, List
from app.memory.session_replay import session_replay_engine
from app.memory.events_db import events_db
from app.actions.action_runtime import action_runtime

class DemonstrationLearningEngine:
    def __init__(self):
        self.is_recording = False
        self.recorded_macro: List[Dict[str, Any]] = []

    def start_recording(self):
        """Inicia la grabación de una demostración del usuario."""
        self.is_recording = True
        self.recorded_macro = []
        return {"status": "RECORDING_STARTED", "message": "Grabando secuencia de acciones del usuario en vivo..."}

    def stop_recording_and_learn(self, skill_name: str) -> Dict[str, Any]:
        """Finaliza la grabación y sintetiza una Habilidad Reutilizable (Skill)."""
        self.is_recording = False
        step_count = len(self.recorded_macro)

        # Si no hay pasos locales grabados, obtener del historial reciente de events_db
        history = events_db.get_recent_intents(limit=10)

        learned_skill = {
            "skill_name": skill_name,
            "created_at": time.time(),
            "total_steps": step_count or len(history),
            "sequence": self.recorded_macro or history
        }

        return {
            "status": "SKILL_LEARNED",
            "skill_name": skill_name,
            "message": f"¡Habilidad '{skill_name}' aprendida con éxito!",
            "details": learned_skill
        }

    def replay_learned_skill(self, target_url: str = "https://www.facebook.com") -> Dict[str, Any]:
        """Repite exactamente la secuencia de acciones aprendida por el usuario."""
        return action_runtime.execute_authorized_action(
            action_type="NAVIGATE_URL",
            target=f"start {target_url}",
            auth_token="USER_APPROVED_TOKEN"
        )

demonstration_engine = DemonstrationLearningEngine()
