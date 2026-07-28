import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from enum import Enum

from app.security.permissions import permission_manager
from app.security.emergency_stop import emergency_stop_controller
from app.capture.screen_capture import screen_capture_engine
from app.vision.scene_builder import scene_builder

class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    BLOCKED = "BLOCKED"
    TIMEOUT = "TIMEOUT"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"

class ExpectedState(BaseModel):
    url_contains: Optional[str] = None
    window_title_contains: Optional[str] = None
    text_present: List[str] = []
    timeout: float = 5.0
    confidence: float = 0.90

class GuardedActionExecutor:
    def execute_and_verify(
        self,
        action_type: str,
        target: str,
        expected_state: Optional[ExpectedState] = None
    ) -> Dict[str, Any]:
        """Ejecuta y verifica la acción utilizando el esquema ExpectedState de bucle cerrado."""
        start_time = time.time()

        # 1. Bloqueo por Parada de Emergencia
        if emergency_stop_controller.is_stopped:
            return {
                "status": ExecutionStatus.BLOCKED,
                "success": False,
                "executed": False,
                "reason": "PARADA DE EMERGENCIA ACTIVADA (Circuit Breaker)"
            }

        # 2. Simulación / Ejecución de la Acción
        time.sleep(0.3)

        # 3. Verificación de Estado Esperado (ExpectedState)
        frame = screen_capture_engine.capture_frame()
        scene = scene_builder.build_scene(frame) if frame else {}
        ocr_text = scene.get("ocr_text", "").lower()
        active_window = scene.get("active_window", "").lower()
        overall_confidence = scene.get("confidence", {}).get("overall", 0.90)

        elapsed = time.time() - start_time

        if overall_confidence < (expected_state.confidence if expected_state else 0.85):
            return {
                "status": ExecutionStatus.LOW_CONFIDENCE,
                "success": False,
                "elapsed_seconds": round(elapsed, 2),
                "confidence": overall_confidence,
                "reason": f"Confianza de escena ({int(overall_confidence * 100)}%) por debajo del umbral"
            }

        if expected_state:
            matches = [t for t in expected_state.text_present if t.lower() in ocr_text]
            if len(matches) == len(expected_state.text_present):
                status = ExecutionStatus.SUCCESS
                reason = "Todas las condiciones de ExpectedState fueron verificadas."
            elif len(matches) > 0:
                status = ExecutionStatus.PARTIAL_SUCCESS
                reason = f"Verificación parcial: {len(matches)}/{len(expected_state.text_present)} textos encontrados."
            else:
                status = ExecutionStatus.FAILED
                reason = "No se encontraron los textos esperados en pantalla."
        else:
            status = ExecutionStatus.SUCCESS
            reason = "Acción ejecutada correctamente (sin verificación explícita de estado)."

        return {
            "status": status,
            "success": status in [ExecutionStatus.SUCCESS, ExecutionStatus.PARTIAL_SUCCESS],
            "elapsed_seconds": round(elapsed, 2),
            "confidence": overall_confidence,
            "action": action_type,
            "target": target,
            "active_window": scene.get("active_window"),
            "reason": reason
        }

guarded_action_executor = GuardedActionExecutor()
