import time
import io
import mss
from PIL import Image
from typing import Dict, Any, Optional
from app.capture.base import CaptureEngine
from app.event_bus import event_bus
from app.config import config

class FastScreenCapture(CaptureEngine):
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1] if len(self.sct.monitors) > 1 else self.sct.monitors[0]
        self.frame_count = 0
        self.start_time = time.time()
        self.last_latency_ms = 0.0
        self.actual_fps = 0.0
        self.last_jpeg_bytes: Optional[bytes] = None

    def capture_frame(self) -> Image.Image:
        t0 = time.perf_counter()
        try:
            sct_img = self.sct.grab(self.monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img_resized = img.resize((960, 540))

            buffer = io.BytesIO()
            img_resized.save(buffer, format="JPEG", quality=70)
            self.last_jpeg_bytes = buffer.getvalue()

            self.last_latency_ms = round((time.perf_counter() - t0) * 1000, 2)
            self.frame_count += 1

            elapsed = time.time() - self.start_time
            if elapsed >= 1.0:
                self.actual_fps = round(self.frame_count / elapsed, 1)
                self.frame_count = 0
                self.start_time = time.time()

            event_bus.publish("FRAME_CAPTURED", {
                "width": img_resized.width,
                "height": img_resized.height,
                "latency_ms": self.last_latency_ms,
                "fps": self.actual_fps
            })

            return img_resized
        except Exception as e:
            # Recrear instancia mss en caso de error BitBlt de Windows Graphics
            try:
                self.sct = mss.mss()
            except Exception:
                pass

            # Generar cuadro de respaldo limpio
            fallback = Image.new("RGB", (960, 540), color=(15, 23, 42))
            buffer = io.BytesIO()
            fallback.save(buffer, format="JPEG", quality=70)
            self.last_jpeg_bytes = buffer.getvalue()
            return fallback

    def get_stats(self) -> Dict[str, Any]:
        return {
            "actual_fps": self.actual_fps,
            "target_fps": config.target_fps,
            "latency_ms": self.last_latency_ms,
            "resolution": f"{self.monitor['width']}x{self.monitor['height']}"
        }

screen_capture_engine = FastScreenCapture()
