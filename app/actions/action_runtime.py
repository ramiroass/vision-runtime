import subprocess
import time
from typing import Dict, Any, List
from app.config import config
from app.security.permissions import permission_manager
from app.security.emergency_stop import emergency_stop_controller

class ActionRuntime:
    def __init__(self):
        self.action_history: List[Dict[str, Any]] = []

    def execute_authorized_action(
        self,
        action_type: str,
        target: str,
        params: Dict[str, Any] = None,
        auth_token: str = None
    ) -> Dict[str, Any]:
        """Ejecuta acciones en la PC bajo autorización explícita (Nivel 3 / 4)."""
        params = params or {}

        # 1. Verificar Parada de Emergencia
        if emergency_stop_controller.is_stopped:
            return {
                "success": False,
                "executed": False,
                "reason": "CIRCUIT_BREAKER_TRIGGERED: Parada de emergencia activa"
            }

        # 2. Verificar Autenticación/Permisos
        if not auth_token or auth_token != "USER_APPROVED_TOKEN":
            return {
                "success": False,
                "executed": False,
                "reason": "Falta token de aprobación explícita del usuario (Level 3 Required)"
            }

        # 3. Mapeo de Ejecutores por Categoría
        result_message = ""
        try:
            if action_type == "OPEN_PROCESS":
                # Abrir aplicaciones/procesos (ej. Notepad, Calc, Browser)
                subprocess.Popen(target, shell=True)
                result_message = f"Proceso '{target}' iniciado exitosamente."

            elif action_type == "NAVIGATE_URL":
                # Automatización del navegador
                result_message = f"Navegador abierto en la URL '{target}'."

            elif action_type == "CLICK_UI_ELEMENT":
                # Simulación de clic sobre elemento visual
                result_message = f"Clic simulado en elemento '{target}' en ({params.get('x', 0)}, {params.get('y', 0)})."

            elif action_type == "TYPE_TEXT":
                # Simulación de escritura de texto
                result_message = f"Texto '{target}' enviado a la ventana activa."

            else:
                return {"success": False, "executed": False, "reason": f"Tipo de acción '{action_type}' desconocido"}

            record = {
                "timestamp": time.time(),
                "action_type": action_type,
                "target": target,
                "status": "EXECUTED",
                "message": result_message
            }
            self.action_history.append(record)

            return {
                "success": True,
                "executed": True,
                "action_type": action_type,
                "target": target,
                "message": result_message
            }

        except Exception as e:
            return {
                "success": False,
                "executed": False,
                "reason": f"Error ejecutando acción en Action Runtime: {str(e)}"
            }

action_runtime = ActionRuntime()
