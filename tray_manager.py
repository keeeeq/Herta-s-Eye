"""
黑塔之眼 - 系统托盘管理器
右下角图标，右键可退出服务
"""

import subprocess
import sys
import os
import signal

# 需要安装: pip install pystray pillow
try:
    from pystray import Icon, MenuItem, Menu
    from PIL import Image, ImageDraw
except ImportError:
    print("请先安装依赖: pip install pystray pillow")
    sys.exit(1)

# 全局进程引用
backend_proc = None
frontend_proc = None

def create_icon_image():
    """创建一个简单的图标"""
    img = Image.new('RGB', (64, 64), color=(5, 5, 16))
    draw = ImageDraw.Draw(img)
    # 画一个简单的眼睛形状
    draw.ellipse([12, 20, 52, 44], outline=(0, 243, 255), width=2)
    draw.ellipse([28, 28, 36, 36], fill=(165, 109, 226))
    return img

def start_services():
    """启动后端和前端服务"""
    global backend_proc, frontend_proc
    
    # 切换到脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 启动后端 (隐藏窗口)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "backend.main"],
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    
    # 等待后端启动
    import time
    time.sleep(2)
    
    # 启动前端 (隐藏窗口)
    frontend_proc = subprocess.Popen(
        ["streamlit", "run", "frontend/app.py", 
         "--server.address", "0.0.0.0", 
         "--server.headless", "true"],
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    
    return True

def stop_services(icon=None, item=None):
    """停止所有服务并退出"""
    global backend_proc, frontend_proc
    
    if backend_proc:
        backend_proc.terminate()
    if frontend_proc:
        frontend_proc.terminate()
    
    # 强制杀死残留进程
    os.system('taskkill /F /IM python.exe >nul 2>&1')
    os.system('taskkill /F /IM streamlit.exe >nul 2>&1')
    
    if icon:
        icon.stop()
    
    sys.exit(0)

def open_browser(icon, item):
    """打开浏览器"""
    import webbrowser
    webbrowser.open("http://localhost:8501")

def main():
    # 启动服务
    print("正在启动服务...")
    start_services()
    print("服务已启动")
    
    # 创建托盘图标
    menu = Menu(
        MenuItem("打开界面", open_browser),
        MenuItem("退出", stop_services)
    )
    
    icon = Icon(
        "Herta's Eye",
        create_icon_image(),
        "黑塔之眼 - 运行中",
        menu
    )
    
    # 运行托盘图标 (阻塞)
    icon.run()

if __name__ == "__main__":
    main()
