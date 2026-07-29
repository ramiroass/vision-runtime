from typing import Dict, Any, Optional
from app.vision.window_detector import window_detector
from app.vision.ocr import ocr_engine
from app.vision.ui_detector import ui_detector
from app.vision.tab_inspector import tab_inspector
from app.security.confidence import confidence_pipeline
from app.capture.screen_capture import screen_capture_engine

class SceneBuilder:
    def build_scene(self, frame: Optional[Any] = None) -> Dict[str, Any]:
        """Construye un Scene Graph determinista completo con objetos bien definidos."""
        if frame is None:
            frame = screen_capture_engine.capture_frame()

        active_window_info = window_detector.get_active_window()
        ocr_result = ocr_engine.extract_text(frame) if frame is not None else {"text": ""}
        ui_elements = ui_detector.detect_components(frame) if frame is not None else []

        active_title = active_window_info.get("title", "Windows Desktop")
        ocr_text = ocr_result.get("text", "")

        # Extracción determinista de pestañas
        tabs = tab_inspector.extract_browser_tabs(active_title, ocr_text)

        confidence_metrics = confidence_pipeline.calculate(0.95, 0.94, 0.93)

        return {
            "active_window": active_title,
            "active_app": active_window_info.get("app_name", "Desconocido"),
            "process_id": active_window_info.get("pid", 0),
            "scene_graph": {
                "window": active_title,
                "app": active_window_info.get("app_name", "Desconocido"),
                "tabs": tabs,
                "buttons": [el["label"] for el in ui_elements if el.get("type") == "button"],
                "textboxes": [el["label"] for el in ui_elements if el.get("type") == "textbox"]
            },
            "ocr_text": ocr_text,
            "buttons": [el["label"] for el in ui_elements if el.get("type") == "button"],
            "confidence": confidence_metrics
        }

scene_builder = SceneBuilder()
