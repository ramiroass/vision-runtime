from typing import Dict, Any, List
from app.config import config

class PermissionManager:
    def __init__(self):
        self.allowed_actions = ["read", "observe", "plan", "simulate"]
        self.restricted_actions = ["click", "type", "execute_command"]

    def is_action_permitted(self, action_type: str, confidence_score: float) -> Dict[str, Any]:
        """Evalúa si una acción está permitida bajo las políticas de seguridad actuales."""
        if action_type in self.allowed_actions:
            return {"permitted": True, "reason": "Acción de lectura/percepción permitida por defecto"}

        if not config.autonomous_mode:
            return {
                "permitted": False,
                "reason": "MODO_AUTÓNOMO_DESACTIVADO: Las acciones de modificación requieren aprobación explícita"
            }

        if confidence_score < 0.85:
            return {
                "permitted": False,
                "reason": f"CIRCUIT_BREAKER: La confianza ({int(confidence_score * 100)}%) es menor al umbral mínimo del 85%"
            }

        return {"permitted": True, "reason": "Acción permitida bajo supervisión autónoma"}

permission_manager = PermissionManager()
