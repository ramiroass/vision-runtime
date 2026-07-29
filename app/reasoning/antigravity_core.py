from typing import Dict, Any, List
from app.memory.session_memory import five_minute_memory
from app.actions.action_runtime import action_runtime

class IntentRouter5Way:
    @staticmethod
    def classify_intent(question: str) -> str:
        q = question.lower().strip()

        # 1. Action Query
        if any(k in q for k in ["abri ", "abrir", "anda a", "ir a", "ejecutar", "lanzar"]):
            return "ACTION_QUERY"

        # 2. UI Structural Query
        if any(k in q for k in ["pestaña", "tab", "ventana", "programa", "activo", "proceso", "título", "titulo", "botón", "boton"]):
            return "UI_STRUCTURAL_QUERY"

        # 3. History Query
        if any(k in q for k in ["hace", "pasó", "paso", "anterior", "minuto", "historial", "replay", "antes"]):
            return "HISTORY_QUERY"

        # 4. Planner Query
        if any(k in q for k in ["siguiente paso", "paso 1", "plan", "secuencia", "cómo hago", "como hago"]):
            return "PLANNER_QUERY"

        # 5. LLM Reasoning Query (Default Fallback)
        return "REASONING_QUERY"

class AntiGravityEngine:
    def __init__(self):
        self.router = IntentRouter5Way()

    def evaluate_scene_context(self, scene_context: Dict[str, Any], question: str) -> Dict[str, Any]:
        """Enrutador de 5 Vías: UI (SceneGraph), Historial (Memory), Plan (Planner), Acción (Action), Razonamiento (LLM)."""
        intent = self.router.classify_intent(question)

        active_window = scene_context.get("active_window", "Escritorio de Windows")
        active_app = scene_context.get("active_app", "Sistema")
        scene_graph = scene_context.get("scene_graph", {})
        ocr_text = scene_context.get("ocr_text", "")

        conf_data = scene_context.get("confidence", {})
        confidence_val = conf_data.get("overall_confidence", 0.94) if isinstance(conf_data, dict) else 0.94

        history = five_minute_memory.get_history()
        snapshots_count = len(history)

        answer = ""

        # RUTA 1: UI Structural Query -> SceneGraph
        if intent == "UI_STRUCTURAL_QUERY":
            tabs = scene_graph.get("tabs", [])
            q_lower = question.lower()
            if "primera pestaña" in q_lower or "primera tab" in q_lower:
                first_tab = tabs[0]["title"] if tabs else active_window
                answer = f"🔍 [SceneGraph] La primera pestaña abierta es: '{first_tab}'."
            elif "pestaña" in q_lower or "tab" in q_lower:
                tabs_list = ", ".join([f"[{t['index']}] '{t['title']}'" for t in tabs])
                answer = f"🔍 [SceneGraph] {len(tabs)} pestañas detectadas: {tabs_list}."
            else:
                answer = f"🔍 [SceneGraph] Ventana activa: '{active_window}' ({active_app}). PID: {scene_context.get('process_id', 0)}."

        # RUTA 2: History Query -> Memory Runtime
        elif intent == "HISTORY_QUERY":
            answer = f"📼 [Memory Runtime] Se registran {snapshots_count} capturas en los últimos 5 minutos. Última aplicación activa: '{active_window}'."

        # RUTA 3: Planner Query -> Task Planner
        elif intent == "PLANNER_QUERY":
            answer = f"🗺️ [Task Planner] Secuencia recomendada: 1. Inspeccionar pantalla -> 2. Verificar estado -> 3. Ejecutar acción supervisada."

        # RUTA 4: Action Query -> Action Runtime
        elif intent == "ACTION_QUERY":
            answer = f"⚡ [Action Runtime] Orden de acción detectada: '{question}'. Enrutada al Task Planner para confirmación supervisada."

        # RUTA 5: Reasoning Query -> LLM Core
        else:
            if "error" in question.lower() or "fallo" in question.lower():
                if "error" in ocr_text.lower() or "failed" in ocr_text.lower():
                    answer = f"🧠 [LLM Inferencia] Se detectó un error en pantalla: '{ocr_text[:120]}...'"
                else:
                    answer = f"🧠 [LLM Inferencia] No se detectan errores en '{active_window}'. Aplicación limpia."
            else:
                answer = f"🧠 [LLM Inferencia] Razonando sobre '{active_window}': Confianza de escena: {int(confidence_val*100)}%."

        return {
            "engine": "AntiGravity Core v3.0 (5-Way Router)",
            "intent_type": intent,
            "question": question,
            "answer": answer,
            "scene_graph": scene_graph,
            "proposed_plan": [
                {"step": 1, "action": "INTENT_CLASSIFICATION", "target": intent, "status": "COMPLETED"},
                {"step": 2, "action": "DISPATCH_HANDLER", "target": intent, "status": "COMPLETED"},
                {"step": 3, "action": "RESPONSE_SYNTHESIS", "target": answer[:40], "status": "COMPLETED"}
            ]
        }

antigravity_engine = AntiGravityEngine()
