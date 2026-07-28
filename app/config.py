import os
from pydantic import BaseModel

class SystemConfig(BaseModel):
    app_name: str = "Vision Runtime"
    version: str = "1.0.0"
    target_fps: int = 20  # Configurable: 10, 20, 30, 60
    autonomous_mode: bool = False  # NEVER execute actions by default
    perception_mode: str = "OBSERVE"  # OBSERVE, PLAN, SIMULATE, EXECUTE
    safety_policy: str = "STRICT"
    max_memory_queue: int = 1000
    host: str = "127.0.0.1"
    port: int = 8080

config = SystemConfig()
