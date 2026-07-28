from typing import Dict, Any
from app.config import config

class PolicyEngine:
    def __init__(self):
        self.emergency_stop_triggered = False

    def evaluate_action_proposal(self, action_type: str, target: str) -> Dict[str, Any]:
        """Evalúa una acción propuesta contra las políticas de seguridad estrictas."""
        if self.emergency_stop_triggered:
            return {
                "policy_status": "DENIED",
                "reason": "EMERGENCY_STOP_ACTIVE",
                "requires_user_approval": True,
                "can_execute": False
            }

        if not config.autonomous_mode:
            return {
                "policy_status": "PROPOSED_ONLY",
                "reason": "AUTONOMOUS_MODE_OFF (Solo observación y propuestas)",
                "requires_user_approval": True,
                "can_execute": False
            }

        return {
            "policy_status": "PENDING_APPROVAL",
            "reason": "Requiere confirmación explícita del usuario",
            "requires_user_approval": True,
            "can_execute": False
        }

policy_engine = PolicyEngine()
