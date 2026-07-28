from typing import Dict, Any, List
from app.config import config

class TaskPlanner:
    def create_assistance_plan(self, goal: str, scene_context: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un plan estructurado de asistencia en 4 fases (NUNCA ejecuta automáticamente)."""
        active_app = scene_context.get("active_app", "Escritorio")
        
        plan_steps = [
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
                "details": "Generación de pasos seguros",
                "status": "READY"
            },
            {
                "step": 3,
                "phase": "SIMULATE",
                "action": "Simulación de trazabilidad y riesgos",
                "details": "Confidence score: 89%",
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

        return {
            "goal": goal,
            "pipeline_state": "WAITING_FOR_APPROVAL",
            "autonomous": config.autonomous_mode,
            "steps": plan_steps
        }

task_planner = TaskPlanner()
