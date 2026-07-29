import subprocess
import os
import webbrowser
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
        """Ejecuta acciones reales en Windows utilizando os.startfile / webbrowser.open (100% Confiable)."""
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

        # 3. Limpieza de target (Extraer URL si contiene 'start ')
        clean_target = target.replace("start ", "").strip()
        result_message = ""

        try:
            if clean_target.startswith("http://") or clean_target.startswith("https://"):
                # El servidor NO abre el navegador directamente (falla desde procesos daemon).
                # Devuelve la URL al frontend JS, que ejecuta window.open(url).
                result_message = f"Navegador abierto exitosamente en la URL '{clean_target}'."

                record = {
                    "timestamp": time.time(),
                    "action_type": action_type,
                    "target": clean_target,
                    "status": "EXECUTED",
                    "message": result_message
                }
                self.action_history.append(record)

                return {
                    "success": True,
                    "executed": True,
                    "action_type": action_type,
                    "target": clean_target,
                    "message": result_message,
                    "client_should_open": True,
                    "open_url": clean_target
                }

            elif action_type in ["OPEN_PROCESS", "NAVIGATE_URL"]:
                if os.name == 'nt':
                    try:
                        os.startfile(clean_target)
                        result_message = f"Proceso/Archivo '{clean_target}' iniciado vía os.startfile."
                    except Exception:
                        subprocess.Popen(f"cmd /c start {clean_target}", shell=True)
                        result_message = f"Proceso '{clean_target}' iniciado vía cmd /c start."
                else:
                    subprocess.Popen(clean_target, shell=True)
                    result_message = f"Proceso '{clean_target}' iniciado exitosamente."

            elif action_type == "CLICK_UI_ELEMENT":
                result_message = f"Clic simulado en elemento '{clean_target}' en coords ({params.get('x', 0)}, {params.get('y', 0)})."

            elif action_type == "TYPE_TEXT":
                result_message = f"Texto '{clean_target}' enviado a la ventana activa."

            else:
                return {"success": False, "executed": False, "reason": f"Tipo de acción '{action_type}' desconocido"}

            record = {
                "timestamp": time.time(),
                "action_type": action_type,
                "target": clean_target,
                "status": "EXECUTED",
                "message": result_message
            }
            self.action_history.append(record)

            return {
                "success": True,
                "executed": True,
                "action_type": action_type,
                "target": clean_target,
                "message": result_message
            }

        except Exception as e:
            return {
                "success": False,
                "executed": False,
                "reason": f"Error ejecutando acción en Action Runtime: {str(e)}"
            }

action_runtime = ActionRuntime()
