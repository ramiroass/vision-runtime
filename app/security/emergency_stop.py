from typing import Dict, Any

class EmergencyStopController:
    def __init__(self):
        self.is_stopped = False

    def trigger_emergency_stop(self) -> Dict[str, Any]:
        self.is_stopped = True
        return {
            "emergency_stop": True,
            "status": "CIRCUIT_BREAKER_TRIGGERED",
            "message": "🚨 PARADA DE EMERGENCIA ACTIVADA: Todos los módulos están congelados."
        }

    def reset_emergency_stop(self) -> Dict[str, Any]:
        self.is_stopped = False
        return {
            "emergency_stop": False,
            "status": "NORMAL",
            "message": "🟢 Parada de emergencia rearmada. Sistema en observación."
        }

emergency_stop_controller = EmergencyStopController()
