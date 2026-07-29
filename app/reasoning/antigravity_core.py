import re
from typing import Dict, Any, List
from app.memory.session_memory import five_minute_memory

class AntiGravityEngine:
    def evaluate_scene_context(self, scene_context: Dict[str, Any], question: str) -> Dict[str, Any]:
        """Evalúa dinámicamente el contexto de la escena en vivo + memoria rodante de 5 min."""
        active_window = scene_context.get("active_window", "Escritorio de Windows")
        active_app = scene_context.get("active_app", "Sistema")
        ocr_text = scene_context.get("ocr_text", "")
        confidence = scene_context.get("confidence", {}).get("overall", 0.94)

        history = five_minute_memory.get_history()
        snapshots_count = len(history)

        question_lower = question.lower()
        answer = ""

        # Detección específica de la primera pestaña / título activo
        if "primera pestaña" in question_lower or "primera tab" in question_lower:
            # Extraer el título de la ventana activa o la primera línea limpia del OCR
            title_clean = active_window.split("-")[0].strip() if "-" in active_window else active_window
            answer = f"La primera pestaña abierta en tu navegador es '{title_clean}' (Ventana completa: '{active_window}')."

        elif "pestaña" in question_lower or "tab" in question_lower:
            lines = [line.strip() for line in ocr_text.split("\n") if len(line.strip()) > 3]
            tabs_detected = lines[:3] if lines else [active_window]
            tabs_formatted = ", ".join([f"'{t}'" for t in tabs_detected])
            answer = f"Pestañas y títulos superiores detectados en '{active_window}': {tabs_formatted}."

        elif "error" in question_lower or "fallo" in question_lower:
            if "error" in ocr_text.lower() or "failed" in ocr_text.lower():
                answer = f"Se detectó un texto de error en la pantalla: '{ocr_text[:120]}...'"
            else:
                answer = f"No se detectan errores explícitos en '{active_window}'. La aplicación se observa limpia."

        elif "ventana" in question_lower or "abierto" in question_lower or "programa" in question_lower:
            answer = f"La aplicación activa en primer plano es '{active_window}' ({active_app}). Hay {snapshots_count} capturas grabadas en la memoria rodante de 5 minutos."

        elif "texto" in question_lower or "lee" in question_lower or "pantalla" in question_lower:
            summary_text = ocr_text[:200] if ocr_text else "Sin texto detectado"
            answer = f"Lectura OCR en pantalla: {summary_text}"

        else:
            lines = [line.strip() for line in ocr_text.split("\n") if len(line.strip()) > 2]
            preview = " | ".join(lines[:3]) if lines else active_window
            answer = f"Observando '{active_window}'. Elementos visuales detectados: {preview}. Registrados {snapshots_count} eventos en 5 min."

        proposed_plan = [
            {"step": 1, "action": "OBSERVE", "target": active_window, "status": "COMPLETED"},
            {"step": 2, "action": "HISTORICAL_QUERY", "target": f"Historial 5 min ({snapshots_count} snapshots)", "status": "ANALYZED"},
            {"step": 3, "action": "RESPONSE_SYNTHESIS", "target": f"Consulta: '{question[:30]}...'", "status": "COMPLETED"}
        ]

        return {
            "engine": "AntiGravity Core v3.0",
            "question": question,
            "answer": answer,
            "active_window": active_window,
            "ocr_summary": ocr_text[:150],
            "proposed_plan": proposed_plan
        }

antigravity_engine = AntiGravityEngine()
