from PIL import Image
from typing import Dict, Any
from app.vision.frame_diff import frame_diff_analyzer
from app.vision.window_detector import window_detector
from app.vision.ocr import ocr_engine
from app.vision.ui_detector import ui_detector
from app.event_bus import event_bus

class SceneBuilder:
    def build_scene(self, frame: Image.Image) -> Dict[str, Any]:
        """Construye el objeto estructurado JSON Scene Description."""
        diff_info = frame_diff_analyzer.analyze_diff(frame)
        win_info = window_detector.get_active_window()
        ocr_info = ocr_engine.extract_text(frame)
        ui_info = ui_detector.detect_components(frame)

        # Confidence Pipeline
        capture_conf = 0.99
        ocr_conf = ocr_info.get("confidence", 0.90)
        ui_conf = ui_info.get("confidence", 0.85)
        overall_conf = round((capture_conf + ocr_conf + ui_conf) / 3.0, 2)

        scene = {
            "active_window": win_info["window_title"],
            "active_app": win_info["active_app"],
            "changed": diff_info["changed"],
            "change_percent": diff_info["change_percent"],
            "buttons": ui_info["buttons"],
            "inputs": ui_info["inputs"],
            "ocr_text": ocr_info["text"],
            "text_snippets": ocr_info["snippets"],
            "confidence": {
                "capture": capture_conf,
                "ocr": ocr_conf,
                "ui": ui_conf,
                "overall": overall_conf
            }
        }

        # Publicar evento SCENE_PROCESSED en el Event Bus
        event_bus.publish("SCENE_PROCESSED", scene)
        return scene

scene_builder = SceneBuilder()
