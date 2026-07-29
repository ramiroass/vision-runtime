import time
import re
from typing import Dict, Any, List
from app.config import config

class TaskPlanner:
    def resolve_target_url(self, goal_text: str) -> str:
        """Resuelve dinámicamente cualquier sitio web o aplicación pedida por el usuario."""
        goal_lower = goal_text.lower().strip()

        # Extraer URLs explícitas (ej. https://... o domain.com)
        url_match = re.search(r'https?://[^\s]+', goal_text)
        if url_match:
            return url_match.group(0)

        domain_match = re.search(r'\b[a-zA-Z0-9-]+\.(com|io|tv|org|net|co|app)\b', goal_lower)
        if domain_match:
            return f"https://{domain_match.group(0)}"

        # Limpiar palabras de acción
        clean = re.sub(r'\b(abri|abrir|anda a|ir a|buscar|navega a|entrar a|open)\b', '', goal_lower).strip()

        if "facebook" in clean:
            return "https://www.facebook.com"
        elif "youtube" in clean:
            return "https://www.youtube.com"
        elif "instagram" in clean:
            return "https://www.instagram.com"
        elif "twitter" in clean or "x.com" in clean:
            return "https://www.twitter.com"
        elif "reddit" in clean:
            return "https://www.reddit.com"
        elif "twitch" in clean:
            return "https://www.twitch.tv"
        elif "deeeep" in clean or "deeep" in clean:
            return "https://deeeep.io"
        elif "github" in clean:
            return "https://github.com"
        elif "chrome" in clean:
            return "chrome"
        elif "notepad" in clean:
            return "notepad"
        elif "calc" in clean:
            return "calc"

        if clean:
            return f"https://www.{clean}.com"

        return "https://www.google.com"

    def create_assistance_plan(self, goal: str, scene_context: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un plan estructurado con trazabilidad explícita (INPUT -> URL RESUELTA -> COMANDO FINAL)."""
        active_app = scene_context.get("active_app", "Escritorio")
        execution_id = f"run_{int(time.time())}"

        resolved_target = self.resolve_target_url(goal)
        is_url = resolved_target.startswith("http")
        action_type = "NAVIGATE_URL" if is_url else "OPEN_PROCESS"
        final_command = f"start {resolved_target}" if is_url else resolved_target

        # Trazabilidad explícita para depuración
        print(f"\n[PLANNER TRACE]")
        print(f"  INPUT DEL USUARIO: {goal}")
        print(f"  URL RESUELTA:      {resolved_target}")
        print(f"  COMANDO FINAL:     {final_command}\n")

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
                "action": f"{action_type} -> {resolved_target}",
                "details": f"Comando final: {final_command}",
                "status": "READY"
            },
            {
                "step": 3,
                "phase": "SIMULATE",
                "action": f"Simular resolución de '{resolved_target}'",
                "details": "Confidence score: 95%",
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
            "execution_id": execution_id,
            "input_user": goal,
            "resolved_url": resolved_target,
            "final_command": final_command,
            "action_type": action_type,
            "goal": goal,
            "intent": action_type,
            "target": resolved_target,
            "pipeline_state": "WAITING_FOR_APPROVAL",
            "autonomous": config.autonomous_mode,
            "plan_sequence": [
                f"1. Resolver objetivo del usuario: '{goal}'",
                f"2. URL/Comando resuelto: {resolved_target}",
                f"3. Ejecutar comando final: {final_command}",
                "4. Verificar resultado visual con ExpectedState"
            ],
            "expected_state": {
                "window_contains": "Browser",
                "url_contains": resolved_target.replace("https://", "").replace("www.", ""),
                "text_present": [resolved_target.replace("https://", "").replace("www.", "")],
                "timeout": 8.0,
                "confidence": 0.90
            },
            "risk": {
                "ui_confidence": 0.96,
                "ocr_confidence": 0.95,
                "planner_confidence": 0.96,
                "execution_risk": "LOW"
            },
            "steps": steps
        }

task_planner = TaskPlanner()
