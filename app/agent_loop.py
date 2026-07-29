import time
from typing import Dict, Any, List

from app.planner.goal_manager import goal_manager
from app.planner.task_planner import task_planner
from app.memory.world_state import world_state_manager
from app.memory.learning import learning_engine
from app.actions.recovery import recovery_engine
from app.actions.guard import guarded_action_executor, ExpectedState, ExecutionStatus
from app.capture.screen_capture import screen_capture_engine
from app.vision.scene_builder import scene_builder

class AgentOSLoopEngine:
    def __init__(self):
        self.execution_queue: List[Dict[str, Any]] = []

    def process_natural_language_goal(self, goal_text: str) -> Dict[str, Any]:
        """Ejecuta el bucle de agente completo (OBSERVE -> PLAN -> ACT -> VERIFY -> LEARN)."""
        start_time = time.time()

        # 1. Goal Manager (Registrar meta a largo plazo)
        goal_obj = goal_manager.set_long_term_goal(goal_text)

        # 2. Vision Runtime & World State (Observe inicial)
        frame = screen_capture_engine.capture_frame()
        scene = scene_builder.build_scene(frame) if frame else {}
        world_state_manager.update_from_scene(scene)

        # 3. Task Planner (Generar contrato de plan)
        plan = task_planner.create_assistance_plan(goal_text, scene)
        resolved_url = plan.get("resolved_url", "https://google.com")
        final_command = plan.get("final_command", f"start {resolved_url}")

        # 4. Action Runtime & Execution Queue (Actuar)
        exec_res = guarded_action_executor.execute_and_verify(
            action_type=plan.get("action_type", "OPEN_PROCESS"),
            target=final_command,
            expected_state=ExpectedState(
                url_contains=resolved_url.replace("https://", "").replace("www.", ""),
                confidence=0.85
            )
        )

        elapsed = round(time.time() - start_time, 2)

        # 5. Learning Engine (Registrar experiencia)
        learning_engine.record_experience(
            goal=goal_text,
            plan=plan.get("plan_sequence", []),
            status=exec_res.get("status", "SUCCESS"),
            duration_seconds=elapsed
        )

        return {
            "pipeline": "Desktop -> Capture -> Scene -> WorldState -> Memory -> Planner -> Skills -> Executor -> Verifier -> Learning",
            "goal": goal_text,
            "execution_id": plan.get("execution_id"),
            "world_state": world_state_manager.get_world_state(),
            "execution_result": exec_res,
            "learnings": learning_engine.get_learnings_summary(),
            "elapsed_seconds": elapsed
        }

agent_os_loop_engine = AgentOSLoopEngine()
