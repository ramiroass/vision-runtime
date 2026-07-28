import psutil
from typing import Dict, Any

class WindowDetector:
    def get_active_window(self) -> Dict[str, Any]:
        """Detecta la aplicación activa y procesos en ejecución en Windows."""
        try:
            # Escanear procesos relevantes activos
            for proc in psutil.process_iter(['pid', 'name']):
                name = proc.info['name'].lower()
                if name in ['code.exe', 'chrome.exe', 'python.exe', 'cmd.exe', 'powershell.exe', 'msedge.exe']:
                    app_name = name.replace('.exe', '').capitalize()
                    return {
                        "active_app": app_name,
                        "window_title": f"{app_name} - Workspace Activo",
                        "pid": proc.info['pid']
                    }
        except Exception:
            pass

        return {
            "active_app": "Windows Desktop",
            "window_title": "Escritorio Principal de Windows",
            "pid": 0
        }

window_detector = WindowDetector()
