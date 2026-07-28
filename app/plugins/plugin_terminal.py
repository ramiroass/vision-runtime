from typing import Dict, Any
from app.plugins.base import VisionPlugin

class TerminalObserverPlugin(VisionPlugin):
    @property
    def plugin_name(self) -> str:
        return "plugin_terminal"

    @property
    def description(self) -> str:
        return "Observador de consolas Terminal, PowerShell y CMD"

    def analyze(self, scene_context: Dict[str, Any]) -> Dict[str, Any]:
        text = scene_context.get("ocr_text", "")
        has_error = "error" in text.lower() or "failed" in text.lower()
        return {
            "plugin": self.plugin_name,
            "terminal_detected": "cmd" in scene_context.get("active_app", "").lower(),
            "has_error_in_logs": has_error,
            "recommendation": "Revisar logs de ejecución en busca de excepciones" if has_error else "Terminal ejecutando normalmente"
        }

terminal_plugin = TerminalObserverPlugin()
