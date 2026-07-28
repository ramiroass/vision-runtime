from typing import Dict, List, Any
from pydantic import BaseModel

class PluginCapability(BaseModel):
    name: str
    description: str
    can_read: List[str]
    can_write: List[str]
    requires: List[str]
    confidence: float
    estimated_latency_ms: int

class CapabilitiesRegistry:
    def __init__(self):
        self._capabilities: Dict[str, PluginCapability] = {}

    def register(self, capability: PluginCapability):
        self._capabilities[capability.name] = capability

    def get_capabilities(self) -> List[Dict[str, Any]]:
        return [c.model_dump() for c in self._capabilities.values()]

capabilities_registry = CapabilitiesRegistry()
capabilities_registry.register(PluginCapability(
    name="plugin_github",
    description="Observador y analizador especializado de GitHub",
    can_read=["browser", "filesystem"],
    can_write=["browser"],
    requires=["login"],
    confidence=0.94,
    estimated_latency_ms=180
))
capabilities_registry.register(PluginCapability(
    name="plugin_terminal",
    description="Observador y analizador de consolas Terminal/CMD",
    can_read=["terminal", "process"],
    can_write=["terminal"],
    requires=[],
    confidence=0.96,
    estimated_latency_ms=45
))
