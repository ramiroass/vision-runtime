"""
AntiGravity Bridge Client - Enlace entre la Inteligencia Artificial y el Vision Runtime Platform.
"""

import urllib.request
import json
import time

VISION_RUNTIME_URL = "http://127.0.0.1:8080"

def get_raw_world_state():
    """Obtiene el estado puro del escritorio (SceneGraph + OCR) sin LLM."""
    try:
        req = urllib.request.urlopen(f"{VISION_RUNTIME_URL}/api/world")
        return json.loads(req.read().decode())
    except Exception as e:
        return {"error": f"No se pudo conectar con Vision Runtime: {e}"}

def ask_vision_runtime(question: str):
    """Envía una pregunta de razonamiento o estructura al runtime."""
    try:
        data = json.dumps({"question": question}).encode('utf-8')
        req = urllib.request.Request(
            f"{VISION_RUNTIME_URL}/api/question",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        res = urllib.request.urlopen(req)
        return json.loads(res.read().decode())
    except Exception as e:
        return {"error": f"Error en consulta: {e}"}

def execute_authorized_plan(goal: str):
    """Genera y ejecuta automáticamente una orden autorizada en tu PC."""
    try:
        # 1. Generar plan
        plan_req = urllib.request.Request(
            f"{VISION_RUNTIME_URL}/api/planner/plan",
            data=json.dumps({"goal": goal}).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        plan_res = json.loads(urllib.request.urlopen(plan_req).read().decode())
        
        target = plan_res.get("final_command") or f"start {plan_res.get('resolved_url', 'google.com')}"
        action_type = plan_res.get("action_type", "OPEN_PROCESS")

        # 2. Autorizar y ejecutar en PC
        exec_req = urllib.request.Request(
            f"{VISION_RUNTIME_URL}/api/actions/authorize-execute",
            data=json.dumps({
                "action_type": action_type,
                "target": target,
                "auth_token": "USER_APPROVED_TOKEN"
            }).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        return json.loads(urllib.request.urlopen(exec_req).read().decode())
    except Exception as e:
        return {"error": f"Error ejecutando plan: {e}"}

if __name__ == "__main__":
    print("🤖 Conectando AntiGravity Bridge con Vision Runtime Platform...")
    world = get_raw_world_state()
    print("\n[ESTADO DEL MUNDO EN VIVO]:")
    print(f"  Ventana Activa: {world.get('active_window')}")
    print(f"  OCR Summary:    {world.get('ocr_summary')}")
