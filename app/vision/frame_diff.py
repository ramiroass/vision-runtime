from PIL import Image, ImageChops, ImageStat
from typing import Dict, Any, Tuple

class FrameDiffAnalyzer:
    def __init__(self):
        self.last_frame: Image.Image = None

    def analyze_diff(self, current_frame: Image.Image) -> Dict[str, Any]:
        """Calcula el porcentaje de cambio visual entre el frame actual y el anterior."""
        if self.last_frame is None or self.last_frame.size != current_frame.size:
            self.last_frame = current_frame
            return {"changed": True, "change_percent": 100.0}

        diff = ImageChops.difference(current_frame, self.last_frame)
        stat = ImageStat.Stat(diff)
        diff_val = sum(stat.mean) / (len(stat.mean) * 255.0) * 100.0

        self.last_frame = current_frame
        changed = diff_val > 0.5  # Umbral de cambio

        return {
            "changed": changed,
            "change_percent": round(diff_val, 2)
        }

frame_diff_analyzer = FrameDiffAnalyzer()
