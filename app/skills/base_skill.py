from abc import ABC, abstractmethod
from typing import Dict, Any
from app.actions.guard import ExecutionStatus

class BaseSkill(ABC):
    @property
    @abstractmethod
    def skill_name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta una habilidad de alto nivel que encapsula múltiples acciones atómicas."""
        pass
