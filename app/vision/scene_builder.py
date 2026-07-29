from typing import Dict, Any
from app.vision.window_detector import window_detector
from app.vision.ocr import ocr_engine
from app.vision.ui_detector import ui_detector
from app.vision.tab_inspector import tab_inspector
from app.security.confidence import confidence_pipeline

class SceneBuilder:
    def build_scene(self, frame) -> Dict[str, Any]:
        """Construye un Scene Graph determinista completo con objetos bien definidos."""
        active_window_info = window_detector.get_active_window_info()
        ocr_result = ocr_engine.extract_text(frame) if frame else {"text": ""}
        ui_elements = ui_detector.detect_components(frame) if frame else []

        active_title = active_window_info.get("title", "Windows Desktop")
        ocr_text = ocr_result.get("text", "")

        # Extracción determinista de pestañas
        tabs = tab_inspector.extract_browser_tabs(active_title, ocr_text)

        confidence_metrics = confidence_pipeline.calculate_stage_confidence({
            "frame": frame,
            "ocr_text": ocr_text,
            "ui_elements": ui_elements
        })

        return {
            "active_window": active_title,
            "active_app": active_window_info.get("app_name", "Desconocido"),
            "process_id": active_window_info.get("pid", 0),
            "scene_graph": {
                "window": active_title,
                "app": active_window_info.get("app_name", "Desconocido"),
                "tabs": tabs,
                "buttons": [el["label"] for el in ui_elements if el["type"] == "button"],
                "textboxes": [el["label"] for el in ui_elements if el["type"] == "textbox"]
            },
            "ocr_text": ocr_text,
            "buttons": [el["label"] for el in ui_elements if el["type"] == "button"],
            "confidence": confidence_metrics
        }

scene_builder = SceneBuilder()
