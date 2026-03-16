from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": False})

import os
import time
import numpy as np
import carb
from omni.isaac.core import World
from omni.isaac.core.utils.stage import open_stage
from omni.isaac.core.utils.prims import get_prim_at_path, set_prim_attribute_value
from omni.isaac.franka import Franka # Franka 전용 클래스 사용
import omni.kit.viewport.utility as vp_utils

# 1. USD 환경 로드
usd_path = os.path.expanduser("~/isaac_vr_project/stack_blocks_with_human.usd")
open_stage(usd_path)

# 2. 월드 설정 (60 FPS 고정)
world = World(physics_dt=1.0/60.0, rendering_dt=1.0/60.0)

# ---------------------------------------------------------
# 3. USD에 이미 있는 로봇 불러오기 (경로: /Franka)
# Franka 클래스를 사용하면 그리퍼 제어와 관절 관리가 매우 편해집니다.
my_robot = world.scene.add(Franka(prim_path="/Franka", name="my_franka"))
# ---------------------------------------------------------

world.reset()

# 프레임 제한 설정 (Jitter 방지)
settings = carb.settings.get_settings()
settings.set("/app/runLoops/main/rateLimitEnabled", True)
settings.set("/app/runLoops/main/rateLimitFrequency", 60)

# 카메라 설정
try:
    viewport_api = vp_utils.get_active_viewport_and_window()[0]
    viewport_api.set_active_camera("/World/Human_Camera")
except:
    pass

# 4. SSVEP 자극 설정 (눈 보호 Soft Pulse 모드)
# VR 환경을 고려해 Intensity를 500으로 낮추고 부드럽게 깜빡이게 설정
stimuli_mat = {
    "Green_Mat": {"path": "/World/Looks/Green_Mat", "freq": 20.0, "max_intensity": 2000.0},
    "Red_Mat": {"path": "/World/Looks/Red_Mat", "freq": 10.0, "max_intensity": 2000.0},
}

print("시뮬레이션 시작! 로봇(/Franka) 연결 완료.")

while simulation_app.is_running():
    t = time.time()
    
    # 5. 부드러운 SSVEP 점멸 로직
    for name, info in stimuli_mat.items():
        raw_sine = np.sin(2 * np.pi * info["freq"] * t)
        pulse_ratio = (raw_sine + 1.0) / 2.0 
        current_intensity = info["max_intensity"] * pulse_ratio

        shader_path = f"{info['path']}/Shader"
        if get_prim_at_path(shader_path):
            try:
                set_prim_attribute_value(shader_path, "inputs:emissive_intensity", current_intensity)
            except:
                set_prim_attribute_value(info['path'], "inputs:emissive_intensity", current_intensity)

    world.step(render=True)

simulation_app.close()