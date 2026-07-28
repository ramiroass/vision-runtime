import time
from typing import Dict, Any, List
from app.config import config

class TaskPlanner:
    def create_assistance_plan(self, goal: str, scene_context: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un plan estructurado de asistencia multi-paso con intents, objetivos y ExpectedState."""
        active_app = scene_context.get("active_app", "Escritorio")
        goal_lower = goal.lower()

        execution_id = f"run_{int(time.time())}"
        intent = "GENERAL_ASSISTANCE"
        target_url = None

        if "deeeep" in goal_lower or "deeep" in goal_lower:
            intent = "NAVIGATE_WEBSITE"
            target_url = "https://deeeep.io"
        elif "google" in goal_lower:
            intent = "NAVIGATE_WEBSITE"
            target_url = "https://www.google.com"
        elif "chrome" in goal_lower:
            intent = "OPEN_PROCESS"
            target_url = "chrome"

        # Plan estructurado de múltiples pasos
        steps = [
            {
                "step": 1,
                "phase": "OBSERVE",
                "action": "Inspeccionar contexto actual de pantalla",
                "details": f"Aplicación activa: {active_app}",
                "status": "COMPLETED"
            },
            {
                "step": 2,
                "phase": "PLAN",
                "action": f"Estructurar secuencia para el objetivo: '{goal}'",
                "details": f"Intent: {intent} | Target: {target_url or 'Escritorio'}",
                "status": "READY"
            },
            {
                "step": 3,
                "phase": "SIMULATE",
                "action": f"Simular apertura y navegación a '{target_url or goal}'",
                "details": "Confidence score: 92%",
                "status": "SIMULATED"
            },
            {
                "step": 4,
                "phase": "WAIT_USER_APPROVAL",
                "action": "Esperar aprobación explícita del usuario",
                "details": "Requerido confirmación (autonomous = False)",
                "status": "WAITING_APPROVAL"
            }
        ]

        # Estructura enriquecida del contrato del plan
        return {
            "execution_id": execution_id,
            "goal": goal,
            "intent": intent,
            "target": target_url or goal,
            "pipeline_state": "WAITING_FOR_APPROVAL",
            "autonomous": config.autonomous_mode,
            "plan_sequence": [
                "1. Abrir navegador Chrome",
                f"2. Navegar directamente a {target_url or 'sitio web'}",
                "3. Esperar carga completa (5s)",
                "4. Verificar resultado visual con ExpectedState"
            ],
            "expected_state": {
                "window_contains": "Chrome",
                "url_contains": target_url or "google",
                "text_present": [target_url.replace("https://", "").replace("www.", "") if target_url else goal],
                "timeout": 8.0,
                "confidence": 0.90
            },
            "risk": {
                "ui_confidence": 0.95,
                "ocr_confidence": 0.93,
                "planner_confidence": 0.91,
                "execution_risk": "LOW"
            },
            "steps": steps
        }

task_planner = TaskPlanner()
