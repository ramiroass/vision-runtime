from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from PIL import Image

class CaptureEngine(ABC):
    @abstractmethod
    def capture_frame(self) -> Optional[Image.Image]:
        """Captura un único cuadro del escritorio y devuelve un objeto PIL.Image."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Devuelve métricas de rendimiento de la captura (FPS reales, latencia ms)."""
        pass
