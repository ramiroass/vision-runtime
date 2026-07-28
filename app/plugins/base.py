from abc import ABC, abstractmethod
from typing import Dict, Any

class VisionPlugin(ABC):
    @property
    @abstractmethod
    def plugin_name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def analyze(self, scene_context: Dict[str, Any]) -> Dict[str, Any]:
        pass
