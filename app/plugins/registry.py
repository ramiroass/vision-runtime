from typing import Dict, List, Any
from app.plugins.base import VisionPlugin
from app.plugins.plugin_terminal import terminal_plugin
from app.plugins.plugin_github import github_plugin
from app.plugins.plugin_vscode import vscode_plugin

class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, VisionPlugin] = {}
        self.register_plugin(terminal_plugin)
        self.register_plugin(github_plugin)
        self.register_plugin(vscode_plugin)

    def register_plugin(self, plugin: VisionPlugin):
        self._plugins[plugin.plugin_name] = plugin

    def list_plugins(self) -> List[Dict[str, str]]:
        return [
            {"name": p.plugin_name, "description": p.description}
            for p in self._plugins.values()
        ]

    def run_plugin(self, plugin_name: str, scene_context: Dict[str, Any]) -> Dict[str, Any]:
        plugin = self._plugins.get(plugin_name)
        if not plugin:
            return {"error": f"Plugin {plugin_name} no registrado"}
        return plugin.analyze(scene_context)

plugin_registry = PluginRegistry()
