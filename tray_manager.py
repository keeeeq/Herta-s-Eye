"""
黑塔之眼 - 系统托盘管理器 (v1.1)
===============================
功能:
- 右下角系统托盘图标
- 右键菜单: 打开界面 / 退出
- 自动启动后端和前端服务
- 完善的错误处理和日志

依赖: pip install pystray pillow
"""

import subprocess
import sys
import os
import time
import logging
from pathlib import Path

# --- 日志配置 ---
LOG_FILE = Path(__file__).parent / "herta_eye.log"
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("HertaEye")

# --- 依赖检查 ---
def check_dependencies():
    """检查必要的依赖是否已安装"""
    missing = []
    
    try:
        from pystray import Icon, MenuItem, Menu
    except ImportError:
        missing.append("pystray")
    
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        missing.append("Pillow")
    
    if missing:
        logger.error(f"缺少依赖: {', '.join(missing)}")
        logger.error("请运行: pip install " + " ".join(missing))
        return False
    
    return True

# --- 全局变量 ---
backend_proc = None
frontend_proc = None
script_dir = Path(__file__).parent.resolve()

def create_icon_image():
    """创建托盘图标 (霓虹眼睛)"""
    from PIL import Image, ImageDraw
    
    img = Image.new('RGBA', (64, 64), color=(5, 5, 16, 255))
    draw = ImageDraw.Draw(img)
    # 外圈
    draw.ellipse([8, 18, 56, 46], outline=(0, 243, 255), width=2)
    # 瞳孔
    draw.ellipse([26, 26, 38, 38], fill=(165, 109, 226))
    # 高光
    draw.ellipse([30, 28, 34, 32], fill=(255, 255, 255))
    return img

def start_services():
    """启动后端和前端服务"""
    global backend_proc, frontend_proc
    
    os.chdir(script_dir)
    logger.info(f"工作目录: {script_dir}")
    
    # Windows 隐藏窗口配置
    startupinfo = None
    creationflags = 0
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        creationflags = subprocess.CREATE_NO_WINDOW
    
    # 启动后端
    try:
        backend_cmd = [sys.executable, "-m", "backend.main"]
        backend_proc = subprocess.Popen(
            backend_cmd,
            startupinfo=startupinfo,
            creationflags=creationflags,
            cwd=script_dir
        )
        logger.info(f"后端已启动 (PID: {backend_proc.pid})")
    except Exception as e:
        logger.error(f"后端启动失败: {e}")
        return False
    
    # 等待后端初始化
    time.sleep(3)
    
    # 检查后端是否仍在运行
    if backend_proc.poll() is not None:
        logger.error("后端进程已退出，启动失败")
        return False
    
    # 启动前端
    try:
        frontend_cmd = [
            "streamlit", "run", "frontend/app.py",
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ]
        frontend_proc = subprocess.Popen(
            frontend_cmd,
            startupinfo=startupinfo,
            creationflags=creationflags,
            cwd=script_dir
        )
        logger.info(f"前端已启动 (PID: {frontend_proc.pid})")
    except Exception as e:
        logger.error(f"前端启动失败: {e}")
        stop_services()
        return False
    
    logger.info("所有服务启动成功")
    return True

def stop_services(icon=None, item=None):
    """停止所有服务并退出"""
    global backend_proc, frontend_proc
    
    logger.info("正在停止服务...")
    
    # 终止进程
    for name, proc in [("后端", backend_proc), ("前端", frontend_proc)]:
        if proc and proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                logger.info(f"{name}已停止")
            except subprocess.TimeoutExpired:
                proc.kill()
                logger.warning(f"{name}强制终止")
            except Exception as e:
                logger.error(f"停止{name}失败: {e}")
    
    logger.info("服务已停止")
    
    if icon:
        icon.stop()
    
    sys.exit(0)

def open_browser(icon, item):
    """打开浏览器"""
    import webbrowser
    url = "http://localhost:8501"
    logger.info(f"打开浏览器: {url}")
    webbrowser.open(url)

def get_status_text():
    """获取服务状态"""
    backend_ok = backend_proc and backend_proc.poll() is None
    frontend_ok = frontend_proc and frontend_proc.poll() is None
    
    if backend_ok and frontend_ok:
        return "黑塔之眼 - 运行中 ✅"
    elif backend_ok:
        return "黑塔之眼 - 前端异常 ⚠️"
    elif frontend_ok:
        return "黑塔之眼 - 后端异常 ⚠️"
    else:
        return "黑塔之眼 - 服务异常 ❌"

def main():
    """主入口"""
    logger.info("=" * 40)
    logger.info("黑塔之眼启动中...")
    
    # 检查依赖
    if not check_dependencies():
        input("按 Enter 退出...")
        sys.exit(1)
    
    # 导入 pystray (已确认可用)
    from pystray import Icon, MenuItem, Menu
    
    # 启动服务
    if not start_services():
        logger.error("服务启动失败，请检查日志")
        input("按 Enter 退出...")
        sys.exit(1)
    
    # 创建托盘菜单
    menu = Menu(
        MenuItem("打开界面 (localhost:8501)", open_browser, default=True),
        MenuItem("退出", stop_services)
    )
    
    # 创建托盘图标
    icon = Icon(
        name="HertaEye",
        icon=create_icon_image(),
        title=get_status_text(),
        menu=menu
    )
    
    logger.info("托盘图标已创建，服务就绪")
    
    # 运行 (阻塞)
    icon.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("用户中断")
        stop_services()
    except Exception as e:
        logger.exception(f"未处理的异常: {e}")
        stop_services()
