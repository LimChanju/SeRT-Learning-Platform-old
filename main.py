# Isaac Sim Engine을 불러오고 창을 띄운다
from isaacsim import SimulationApp
simulation_app = SimulationApp({"headless": False})

import os
from onmi.isaac.core import World
from omni.isaac.core.utils.stage import open_stage

# 실험을 진행할 USE 파일 경로 지정
usd_path = os.path.expanduser("~/isaac_vr_project/stack_blocks_with_human.usd")

# 환경을 화면에 띄움
print(f"[{usd_path}] 환경을 불러오는 중...")
open_stage(usd_path)

# 물리 엔진과 시뮬레이션 시간을 관리할 'World'를 생성
world = World()

# 무한 루프: 창이 꺼질 때까지 심류레이션을 계속 돌림
print("Simulation Started.")
while simulation_app.is_running():
    world.step(render=True)

# 창이 닫히면 엔진을 안전하게 종료
simulation_app.close()