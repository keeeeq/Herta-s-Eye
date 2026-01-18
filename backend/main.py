"""
黑塔之眼 - 后端核心 (v5.1 No Mock)
==========================================
游戏玩家优化版:
- 新增 GPU VRAM / 功耗 / 频率 监控
- 使用 Optional[float] 表示不可用数据 (前端可条件隐藏)
- 移除 Mock 模式: DLL 加载失败则直接报错退出
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
from pydantic import BaseModel
import os
import sys
import clr

app = FastAPI(title="Herta's Eye v5.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 数据模型 ---
class SystemStats(BaseModel):
    cpu: Optional[float] = None
    cpu_temp: Optional[float] = None
    ram: Optional[float] = None
    gpu_usage: Optional[float] = None
    gpu_temp: Optional[float] = None
    gpu_vram_used: Optional[float] = None
    gpu_vram_total: Optional[float] = None
    gpu_power: Optional[float] = None
    gpu_clock: Optional[float] = None
    fan_speed: Optional[str] = None

class RoastResponse(BaseModel):
    message: str

# --- 硬件监控 (无 Mock 回退) ---
class HardwareMonitor:
    def __init__(self):
        dll_path = os.path.join(os.getcwd(), "LibreHardwareMonitorLib.dll")
        
        if not os.path.exists(dll_path):
            print(f"❌ 致命错误: DLL 未找到: {dll_path}")
            sys.exit(1)
        
        try:
            clr.AddReference(dll_path)
            from LibreHardwareMonitor.Hardware import Computer
            
            self.computer = Computer()
            self.computer.IsCpuEnabled = True
            self.computer.IsGpuEnabled = True
            self.computer.IsMemoryEnabled = True
            self.computer.IsMotherboardEnabled = True
            self.computer.IsControllerEnabled = True
            self.computer.IsStorageEnabled = False
            self.computer.IsNetworkEnabled = False
            
            self.computer.Open()
            print("✅ 硬件监控初始化成功 (v5.1 - No Mock)")
            
        except Exception as e:
            print(f"❌ 致命错误: DLL 加载失败: {e}")
            sys.exit(1)

    def get_status(self) -> SystemStats:
        cpu_usage = None
        cpu_temp = None
        ram_usage = None
        gpu_usage = None
        gpu_temp = None
        gpu_vram_used = None
        gpu_vram_total = None
        gpu_power = None
        gpu_clock = None
        fan_speeds = []

        for hardware in self.computer.Hardware:
            hardware.Update()
            h_type = str(hardware.HardwareType)

            for sensor in hardware.Sensors:
                s_type = str(sensor.SensorType)
                s_name = sensor.Name
                s_val = sensor.Value
                
                if s_val is None:
                    continue

                # === CPU ===
                if h_type == "Cpu":
                    if s_type == "Load" and s_name == "CPU Total":
                        cpu_usage = round(s_val, 1)
                    if s_type == "Temperature":
                        if "Core" in s_name or "Package" in s_name:
                            if s_val > 0:
                                cpu_temp = round(max(cpu_temp or 0, s_val), 1)

                # === RAM ===
                if h_type == "Memory" and "Total" in hardware.Name:
                    if s_type == "Load" and s_name == "Memory":
                        ram_usage = round(s_val, 1)

                # === GPU ===
                if "Gpu" in h_type:
                    if s_type == "Load" and s_name == "GPU Core":
                        gpu_usage = round(max(gpu_usage or 0, s_val), 1)
                    
                    if s_type == "Temperature":
                        if "Core" in s_name or "Hot Spot" in s_name:
                            if s_val > 0:
                                gpu_temp = round(max(gpu_temp or 0, s_val), 1)
                    
                    if s_type == "SmallData":
                        if s_name == "GPU Memory Used":
                            if s_val > (gpu_vram_used or 0):
                                gpu_vram_used = round(s_val, 0)
                        if s_name == "GPU Memory Total":
                            if s_val > (gpu_vram_total or 0):
                                gpu_vram_total = round(s_val, 0)
                    
                    if s_type == "Power" and "Package" in s_name:
                        gpu_power = round(s_val, 1)
                    
                    if s_type == "Clock" and s_name == "GPU Core":
                        if s_val > (gpu_clock or 0):
                            gpu_clock = round(s_val, 0)
                    
                    if s_type == "Fan":
                        fan_speeds.append(f"{int(s_val)} RPM")

        fan_str = ", ".join(fan_speeds) if fan_speeds else None

        return SystemStats(
            cpu=cpu_usage,
            cpu_temp=cpu_temp,
            ram=ram_usage,
            gpu_usage=gpu_usage,
            gpu_temp=gpu_temp,
            gpu_vram_used=gpu_vram_used,
            gpu_vram_total=gpu_vram_total,
            gpu_power=gpu_power,
            gpu_clock=gpu_clock,
            fan_speed=fan_str
        )

monitor = HardwareMonitor()

# --- 黑塔语录 ---
import random
class HertaAgent:
    ROASTS = [
        "警告：核心温度过高。你是把咖啡倒进机箱里煮了吗？",
        "GPU 要熔化了。在我的空间站里，这种低效是犯罪。",
        "风扇在尖叫。可惜我不是维修工，我是天才。",
        "CPU 占用率过高。你想把这里变成焚烧炉吗？",
        "一切正常。太无聊了，我去测算模拟宇宙。",
        "还没有崩溃吗？真是奇迹。",
        "效率...勉强及格。但离我的标准还差得远。",
        "数据采集完毕。你的电脑就像你一样——勉强能用。",
    ]

    @staticmethod
    def generate_roast(stats: SystemStats) -> str:
        return random.choice(HertaAgent.ROASTS)

# --- API ---
@app.get("/stats", response_model=SystemStats)
async def get_stats():
    return monitor.get_status()

@app.get("/roast", response_model=RoastResponse)
async def get_roast():
    stats = monitor.get_status()
    return RoastResponse(message=HertaAgent.generate_roast(stats))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")
