import re
from typing import Dict, Any, List

class TabInspector:
    def extract_browser_tabs(self, active_window: str, ocr_text: str) -> List[Dict[str, Any]]:
        """Extrae de forma determinista las pestañas del navegador del Scene Graph (sin LLM)."""
        tabs = []
        clean_window_title = active_window.split("-")[0].strip() if "-" in active_window else active_window

        # La primera pestaña siempre es el título de la ventana activa en primer plano
        tabs.append({"index": 0, "title": clean_window_title, "active": True})

        # Parsear líneas de texto OCR en la barra superior
        lines = [l.strip() for l in ocr_text.split("\n") if len(l.strip()) > 3]
        for idx, line in enumerate(lines[:5], start=1):
            if line != clean_window_title and not line.startswith("http"):
                tabs.append({"index": idx, "title": line, "active": False})

        return tabs

tab_inspector = TabInspector()
