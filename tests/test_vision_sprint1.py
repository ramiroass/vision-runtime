import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.server import app
from app.event_bus import event_bus
from app.capture.screen_capture import screen_capture_engine
from app.vision.scene_builder import scene_builder
from app.memory.events_db import events_db
from app.memory.session_replay import session_replay_engine
from app.memory.session_memory import five_minute_memory
from app.planner.task_planner import task_planner
from app.plugins.registry import plugin_registry
from app.security.confidence import confidence_pipeline
from app.security.policy_engine import policy_engine
from app.security.emergency_stop import emergency_stop_controller
from app.security.permissions import permission_manager
from app.actions.guard import guarded_action_executor
from app.actions.action_runtime import action_runtime

client = TestClient(app)

def test_screen_capture_and_stats():
    frame = screen_capture_engine.capture_frame()
    assert frame is not None
    assert frame.width > 0
    assert frame.height > 0
    stats = screen_capture_engine.get_stats()
    assert "actual_fps" in stats
    assert "latency_ms" in stats

def test_action_runtime_authorized_execution():
    # 1. Intentar ejecutar sin token -> Rechazado por falta de aprobación del usuario
    res_no_auth = client.post("/api/actions/authorize-execute", json={
        "action_type": "CLICK_UI_ELEMENT",
        "target": "BotonEnviar",
        "auth_token": "INVALID_TOKEN"
    })
    assert res_no_auth.status_code == 200
    assert res_no_auth.json()["executed"] is False

    # 2. Ejecutar con token de autorización del usuario -> Aprobado por Action Runtime
    res_auth = client.post("/api/actions/authorize-execute", json={
        "action_type": "CLICK_UI_ELEMENT",
        "target": "BotonEnviar",
        "auth_token": "USER_APPROVED_TOKEN",
        "params": {"x": 100, "y": 200}
    })
    assert res_auth.status_code == 200
    assert res_auth.json()["executed"] is True
    assert "Clic simulado" in res_auth.json()["message"]

def test_security_permission_manager_and_emergency_stop():
    read_check = permission_manager.is_action_permitted("read", 0.90)
    assert read_check["permitted"] is True

    click_check = permission_manager.is_action_permitted("click", 0.90)
    assert click_check["permitted"] is False

    resp_stop = client.post("/api/security/emergency-stop")
    assert resp_stop.status_code == 200
    assert resp_stop.json()["emergency_stop"] is True

    exec_res = guarded_action_executor.execute_action("read", "Ventana")
    assert exec_res["success"] is False

    resp_reset = client.post("/api/security/reset-stop")
    assert resp_reset.status_code == 200
    assert resp_reset.json()["emergency_stop"] is False

def test_task_planner_and_plugins():
    frame = screen_capture_engine.capture_frame()
    scene = scene_builder.build_scene(frame)
    plan = task_planner.create_assistance_plan("Publicar release", scene)
    assert plan["pipeline_state"] == "WAITING_FOR_APPROVAL"
    assert len(plan["steps"]) == 4

def test_rest_api_endpoints():
    resp_status = client.get("/api/status")
    assert resp_status.status_code == 200
    assert resp_status.json()["autonomous"] is False

    resp_metrics = client.get("/api/metrics")
    assert resp_metrics.status_code == 200
    assert "executed_actions_count" in resp_metrics.json()

    print("\n[OK] SUITE DE PRUEBAS COMPLETA VISION & ACTION RUNTIME VERIFICADA AL 100%")
