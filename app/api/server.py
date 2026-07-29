from typing import Dict, Any, List
from fastapi import FastAPI, Response, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import psutil
import os
import time

from app.config import config
from app.event_bus import event_bus
from app.capture.screen_capture import screen_capture_engine
from app.vision.scene_builder import scene_builder
from app.vision.ocr import ocr_engine
from app.memory.events_db import events_db
from app.memory.session_replay import session_replay_engine
from app.memory.session_memory import five_minute_memory
from app.memory.world_state import world_state_manager
from app.reasoning.antigravity_core import antigravity_engine
from app.planner.task_planner import task_planner
from app.plugins.registry import plugin_registry
from app.security.policy_engine import policy_engine
from app.security.confidence import confidence_pipeline
from app.security.emergency_stop import emergency_stop_controller
from app.actions.guard import guarded_action_executor
from app.actions.action_runtime import action_runtime

app = FastAPI(
    title="Vision Runtime & Action Runtime Platform",
    version="5.1.0",
    description="Plataforma de Percepción y Control Seguro de PC (Niveles 1 a 5 de Automatización)."
)

class IntentRequest(BaseModel):
    description: str
    status: str = "OK"

class QuestionRequest(BaseModel):
    question: str

class PlanRequest(BaseModel):
    goal: str

class OCRProviderRequest(BaseModel):
    provider: str

class PluginRunRequest(BaseModel):
    plugin_name: str

class AutonomousToggleRequest(BaseModel):
    enable: bool

class ActionExecuteRequest(BaseModel):
    action_type: str
    target: str

class ActionAuthorizeRequest(BaseModel):
    action_type: str
    target: str
    auth_token: str = "USER_APPROVED_TOKEN"
    params: dict = {}

@app.get("/api/status")
def get_status():
    stats = screen_capture_engine.get_stats()
    return {
        "status": "EMERGENCY_STOP" if emergency_stop_controller.is_stopped else "ONLINE",
        "app_name": config.app_name,
        "autonomous": config.autonomous_mode,
        "perception_mode": config.perception_mode,
        "safety_policy": config.safety_policy,
        "emergency_stop": emergency_stop_controller.is_stopped,
        "target_fps": config.target_fps,
        "actual_fps": stats["actual_fps"],
        "latency_ms": stats["latency_ms"],
        "ocr_provider": ocr_engine.active_provider_name
    }

@app.get("/api/metrics")
def get_metrics():
    stats = screen_capture_engine.get_stats()
    cpu_percent = psutil.cpu_percent()
    ram = psutil.virtual_memory()

    return {
        "actual_fps": stats["actual_fps"],
        "target_fps": stats["target_fps"],
        "latency_ms": stats["latency_ms"],
        "cpu_usage_percent": cpu_percent,
        "ram_usage_mb": round(ram.used / (1024 * 1024), 1),
        "confidence_overall": 0.89,
        "autonomous": config.autonomous_mode,
        "emergency_stop": emergency_stop_controller.is_stopped,
        "ocr_provider": ocr_engine.active_provider_name,
        "memory_snapshots_count": len(five_minute_memory.get_history()),
        "registered_plugins_count": len(plugin_registry.list_plugins()),
        "executed_actions_count": len(action_runtime.action_history),
        "events_logged": len(event_bus.get_recent_events())
    }

@app.get("/api/frame")
def get_frame():
    frame = screen_capture_engine.capture_frame()
    if screen_capture_engine.last_jpeg_bytes:
        return Response(content=screen_capture_engine.last_jpeg_bytes, media_type="image/jpeg")
    raise HTTPException(status_code=500, detail="Error capturando pantalla")

@app.get("/api/scene")
def get_scene():
    frame = screen_capture_engine.capture_frame()
    if frame:
        scene = scene_builder.build_scene(frame)
        session_replay_engine.record_step(screen_capture_engine.frame_count, scene)
        five_minute_memory.record_snapshot(scene)
        return scene
    raise HTTPException(status_code=500, detail="Error en percepción de escena")

@app.get("/api/world")
def get_world():
    """Endpoint de auditoría pura del World State y Scene Graph (Sin LLM, sin Intent Router)."""
    try:
        frame = screen_capture_engine.capture_frame()
        scene = scene_builder.build_scene(frame)
        world_state = world_state_manager.get_world_state()
        return {
            "audit": "RAW_WORLD_STATE_PERCEPTION",
            "active_window": scene.get("active_window"),
            "active_app": scene.get("active_app"),
            "process_id": scene.get("process_id"),
            "scene_graph": scene.get("scene_graph"),
            "world_state": world_state,
            "ocr_summary": str(scene.get("ocr_text", ""))[:300],
            "confidence": scene.get("confidence")
        }
    except Exception as e:
        return {
            "audit": "RAW_WORLD_STATE_PERCEPTION_ERROR",
            "error": str(e),
            "world_state": world_state_manager.get_world_state()
        }

@app.get("/api/bridge/status")
def get_bridge_status():
    """Devuelve el estado del enlace activo con el asistente AntiGravity AI."""
    frame = screen_capture_engine.capture_frame()
    scene = scene_builder.build_scene(frame)
    return {
        "status": "CONNECTED_AND_ACTIVE",
        "agent": "AntiGravity AI (Pair Programming Copilot)",
        "timestamp": time.time(),
        "active_window": scene.get("active_window"),
        "ocr_summary": str(scene.get("ocr_text", ""))[:200],
        "bridge_ready": True
    }

@app.post("/api/security/emergency-stop")
def trigger_emergency_stop():
    return emergency_stop_controller.trigger_emergency_stop()

from app.skills.demonstration_learning import demonstration_engine

@app.post("/api/demo/start-recording")
def start_demo_recording():
    """Inicia la grabación de una demostración del usuario."""
    return demonstration_engine.start_recording()

@app.post("/api/demo/stop-and-learn")
def stop_demo_and_learn(request: Dict[str, Any]):
    """Detiene la grabación y sintetiza una Habilidad Reutilizable (Skill)."""
    skill_name = request.get("skill_name", "Macro_Usuario")
    return demonstration_engine.stop_recording_and_learn(skill_name)

@app.post("/api/demo/replay")
def replay_demo_skill(request: Dict[str, Any]):
    """Repite la secuencia aprendida en la PC del usuario."""
    target_url = request.get("target_url", "https://www.facebook.com")
    return demonstration_engine.replay_learned_skill(target_url)

@app.post("/api/security/reset-stop")
def reset_emergency_stop():
    return emergency_stop_controller.reset_emergency_stop()

@app.post("/api/security/autonomous")
def toggle_autonomous(data: AutonomousToggleRequest):
    config.autonomous_mode = data.enable
    return {"success": True, "autonomous_mode": config.autonomous_mode}

@app.post("/api/actions/execute")
def execute_action(data: ActionExecuteRequest):
    return guarded_action_executor.execute_action(data.action_type, data.target)

@app.post("/api/actions/authorize-execute")
def authorize_execute_action(data: ActionAuthorizeRequest):
    return action_runtime.execute_authorized_action(
        data.action_type, data.target, data.params, data.auth_token
    )

@app.get("/api/plugins")
def list_plugins():
    return plugin_registry.list_plugins()

@app.post("/api/plugins/run")
def run_plugin(data: PluginRunRequest):
    frame = screen_capture_engine.capture_frame()
    scene = scene_builder.build_scene(frame) if frame else {}
    return plugin_registry.run_plugin(data.plugin_name, scene)

@app.post("/api/planner/plan")
def create_plan(data: PlanRequest):
    frame = screen_capture_engine.capture_frame()
    scene = scene_builder.build_scene(frame) if frame else {}
    return task_planner.create_assistance_plan(data.goal, scene)

@app.get("/api/memory/history")
def get_memory_history(seconds_ago: int = None):
    return five_minute_memory.get_history(seconds_ago)

@app.get("/api/replay")
def get_replay():
    return session_replay_engine.get_session_replay()

@app.post("/api/ocr/provider")
def set_ocr_provider(data: OCRProviderRequest):
    ocr_engine.set_provider(data.provider)
    return {"success": True, "active_provider": ocr_engine.active_provider_name}

@app.get("/api/events")
def get_events():
    return event_bus.get_recent_events(limit=30)

@app.get("/api/intents")
def get_intents():
    return events_db.get_recent_intents(limit=20)

@app.post("/api/intent")
def log_intent(data: IntentRequest):
    events_db.log_intent(data.description, data.status)
    return {"success": True, "message": "Intención registrada con éxito"}

@app.post("/api/question")
def ask_question(data: QuestionRequest):
    try:
        frame = screen_capture_engine.capture_frame()
        scene = scene_builder.build_scene(frame)
        reasoning = antigravity_engine.evaluate_scene_context(scene, data.question)
        return reasoning
    except Exception as e:
        return {
            "engine": "AntiGravity Core v3.0 (Fallback)",
            "query_type": "ERROR_FALLBACK",
            "question": data.question,
            "answer": f"Error evaluando escena: {str(e)}",
            "proposed_plan": []
        }

# Montar estáticos
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Vision Runtime API en ejecución"}
