from typing import Dict, Any, List
from app.memory.session_memory import five_minute_memory

class AntiGravityReasoningEngine:
    def evaluate_scene_context(self, scene: Dict[str, Any], user_question: str = None) -> Dict[str, Any]:
        """Motor de razonamiento AntiGravity que consulta la escena actual + la memoria de 5 minutos."""
        active_window = scene.get("active_window", "Desconocido")
        active_app = scene.get("active_app", "Desconocido")
        history = five_minute_memory.get_history()

        answer = f"Actualmente observo '{active_window}' ({active_app}). "
        
        if "hace" in user_question.lower() or "paso" in user_question.lower() or "pasó" in user_question.lower():
            if history:
                prev = history[0]
                answer += f"En la memoria reciente (hace {len(history)} frames), estabas trabajando en '{prev['active_window']}'."
            else:
                answer += "Inicié la memoria reciente de 5 minutos."
        else:
            answer += f"La escena tiene un nivel de confianza del {int(scene.get('confidence', {}).get('overall', 0.9) * 100)}%."

        proposed_plan = [
            {"step": 1, "action": "OBSERVE", "target": active_window, "status": "COMPLETED"},
            {"step": 2, "action": "HISTORICAL_QUERY", "target": "Consultar historial de 5 min", "status": "ANALYZED"},
            {"step": 3, "action": "PROPOSE_HELP", "target": "Sugerir optimización de flujo", "status": "WAITING_APPROVAL"}
        ]

        return {
            "engine": "AntiGravity Core v3.0 (Reasoning + 5-Min Memory)",
            "active_context": active_app,
            "historical_frames_count": len(history),
            "answer": answer,
            "proposed_plan": proposed_plan,
            "confidence": scene.get("confidence", {}).get("overall", 0.90)
        }

antigravity_engine = AntiGravityReasoningEngine()
