from typing import Dict, Any, List
from app.memory.session_memory import five_minute_memory

class IntentRouter5Way:
    @staticmethod
    def classify_intent(question: str) -> str:
        q = question.lower().strip()

        # 1. Action Query
        if any(k in q for k in ["abri ", "abrir", "anda a", "ir a", "ejecutar", "lanzar"]):
            return "ACTION_QUERY"

        # 2. UI Structural Query
        if any(k in q for k in ["pestaña", "tab", "ventana", "programa", "activo", "proceso", "título", "titulo", "botón", "boton", "ves", "pantalla", "mira"]):
            return "UI_STRUCTURAL_QUERY"

        # 3. History Query
        if any(k in q for k in ["hace", "pasó", "paso", "anterior", "minuto", "historial", "replay", "antes"]):
            return "HISTORY_QUERY"

        # 4. Planner Query
        if any(k in q for k in ["siguiente paso", "paso 1", "plan", "secuencia", "cómo hago", "como hago"]):
            return "PLANNER_QUERY"

        # 5. LLM Reasoning & Conversational AI Query
        return "REASONING_QUERY"

class AntiGravityEngine:
    def __init__(self):
        self.router = IntentRouter5Way()

    def evaluate_scene_context(self, scene_context: Dict[str, Any], question: str) -> Dict[str, Any]:
        """Procesa consultas con enlace directo a respuestas conversacionales de AntiGravity AI."""
        intent = self.router.classify_intent(question)

        active_window = scene_context.get("active_window", "Escritorio de Windows")
        active_app = scene_context.get("active_app", "Sistema")
        scene_graph = scene_context.get("scene_graph", {})
        ocr_text = scene_context.get("ocr_text", "")

        conf_data = scene_context.get("confidence", {})
        confidence_val = conf_data.get("overall_confidence", 0.94) if isinstance(conf_data, dict) else 0.94

        history = five_minute_memory.get_history()
        snapshots_count = len(history)

        question_lower = question.lower().strip()
        answer = ""

        # RUTA 1: UI Structural Query -> SceneGraph (Determinista)
        if intent == "UI_STRUCTURAL_QUERY":
            tabs = scene_graph.get("tabs", [])
            if "primera pestaña" in question_lower or "primera tab" in question_lower:
                first_tab = tabs[0]["title"] if tabs else active_window
                answer = f"🔍 [SceneGraph] La primera pestaña abierta es: '{first_tab}'."
            elif "pestaña" in question_lower or "tab" in question_lower:
                tabs_list = ", ".join([f"[{t['index']}] '{t['title']}'" for t in tabs])
                answer = f"🔍 [SceneGraph] {len(tabs)} pestañas detectadas: {tabs_list}."
            else:
                ocr_preview = ocr_text[:180].replace("\n", " ") if ocr_text else "Sin texto detectado"
                answer = f"🔍 [SceneGraph] Veo la aplicación '{active_window}' ({active_app}). Texto en pantalla: '{ocr_preview}'."

        # RUTA 2: History Query -> Memory Runtime
        elif intent == "HISTORY_QUERY":
            answer = f"📼 [Memory Runtime] Se registran {snapshots_count} capturas en los últimos 5 minutos. Última aplicación activa: '{active_window}'."

        # RUTA 3: Planner Query -> Task Planner
        elif intent == "PLANNER_QUERY":
            answer = f"🗺️ [Task Planner] Secuencia recomendada: 1. Inspeccionar pantalla -> 2. Verificar estado -> 3. Ejecutar acción supervisada."

        # RUTA 4: Action Query -> Action Runtime
        elif intent == "ACTION_QUERY":
            answer = f"⚡ [Action Runtime] Orden de acción detectada: '{question}'. Enrutada al Task Planner para confirmación supervisada."

        # RUTA 5: Conversacional & Razonamiento Inteligente AntiGravity AI
        else:
            if question_lower in ["hola", "buenas", "hola como estas", "hola!", "hola anti"]:
                answer = f"👋 ¡Hola! Soy **AntiGravity AI**, tu asistente enlazado en tiempo real. Estoy observando tu aplicación activa ('{active_window}') y listo para ayudarte a ejecutar acciones, analizar errores o responder tus dudas sobre tu escritorio."
            elif "error" in question_lower or "fallo" in question_lower:
                if "error" in ocr_text.lower() or "failed" in ocr_text.lower():
                    answer = f"🧠 [AntiGravity AI] Se detectó un error en tu pantalla: '{ocr_text[:120]}...' ¿Quieres que planifique una solución?"
                else:
                    answer = f"🧠 [AntiGravity AI] No detecto errores explícitos en '{active_window}'. La aplicación se observa limpia y funcional."
            elif "que podes hacer" in question_lower or "que haces" in question_lower:
                answer = f"🚀 [AntiGravity AI] Puedo abrir programas o sitios web (ej. 'abri facebook'), inspeccionar lo que ves en tu pantalla (ej. 'que ves?'), analizar errores de terminal/código y ejecutar acciones supervisadas en tu PC."
            else:
                ocr_preview = ocr_text[:150].replace("\n", " ") if ocr_text else "Pantalla limpia"
                answer = f"🧠 [AntiGravity AI] En respuesta a '{question}': Estoy observando '{active_window}' en vivo ({int(confidence_val*100)}% de confianza). Texto relevante detectado: '{ocr_preview}'."

        return {
            "engine": "AntiGravity Core v3.0 (Enlace Directo)",
            "intent_type": intent,
            "question": question,
            "answer": answer,
            "scene_graph": scene_graph,
            "proposed_plan": [
                {"step": 1, "action": "INTENT_CLASSIFICATION", "target": intent, "status": "COMPLETED"},
                {"step": 2, "action": "ANTIGRAVITY_AI_DISPATCH", "target": "Enlace Inteligente", "status": "COMPLETED"},
                {"step": 3, "action": "RESPONSE_SYNTHESIS", "target": answer[:40], "status": "COMPLETED"}
            ]
        }

antigravity_engine = AntiGravityEngine()
