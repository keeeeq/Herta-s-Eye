# 黑塔之眼 (Herta's Eye) 👾

基于 **LibreHardwareMonitor** 的实时硬件监控系统，专为游戏玩家设计。
支持手机远程访问，以赛博朋克风格展示 CPU、GPU、内存等关键指标。

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ 功能特性

- **实时硬件监控**: CPU/GPU 占用率、温度、内存、显存
- **游戏玩家指标**: GPU 功耗 (W)、核心频率 (MHz)、VRAM 占用
- **手机远程访问**: 局域网内手机浏览器即可查看
- **系统托盘管理**: 右下角图标，右键可退出
- **静默后台运行**: 无弹窗，完全隐藏
- **赛博朋克 UI**: 全息蓝 + 霓虹紫的沉浸式界面
- **黑塔语录**: 随机展示《崩坏：星穹铁道》黑塔的吐槽

## 📦 安装

### 1. 克隆仓库
```bash
git clone https://github.com/keeeeq/Herta-s-Eye.git
cd Herta-s-Eye
```

### 2. 创建 Conda 环境
```bash
conda create -n agent python=3.10
conda activate agent
pip install -r requirements.txt
```

### 3. 放置 DLL
从 [LibreHardwareMonitor Releases](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases) 下载，将以下核心 DLL 放入项目根目录:
- `LibreHardwareMonitorLib.dll`
- `HidSharp.dll`
- `System.Memory.dll`
- `System.Buffers.dll`
- `System.Numerics.Vectors.dll`
- `System.Runtime.CompilerServices.Unsafe.dll`

## 🚀 使用方法

### 方式一：显示窗口启动
双击 `start_herta.bat`
- 会显示命令行窗口
- UAC 提权后启动托盘管理器
- 右键托盘图标可"打开界面"或"退出"

### 方式二：静默启动 (推荐)
双击 `silent_launch.vbs`
- 完全无窗口
- UAC 提权后后台运行
- 右下角出现托盘图标

### 手机访问
1. 确保手机与电脑在同一 WiFi
2. 手机浏览器打开: `http://电脑IP:8501`
3. 添加到主屏幕可获得全屏体验

## 📁 项目结构

```
Herta-s-Eye/
├── backend/
│   └── main.py          # FastAPI 后端 (硬件监控)
├── frontend/
│   └── app.py           # Streamlit 前端 (UI)
├── tray_manager.py      # 系统托盘管理器
├── start_herta.bat      # 启动脚本 (有窗口)
├── silent_launch.vbs    # 静默启动器 (推荐)
├── requirements.txt     # Python 依赖
└── README.md
```

## ⚙️ 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | FastAPI + Uvicorn |
| 前端 | Streamlit + Altair |
| 硬件监控 | LibreHardwareMonitor (Pythonnet) |
| 系统托盘 | pystray + Pillow |

## ⚠️ 注意事项

- **需要管理员权限**: CPU 温度读取需要管理员权限
- **仅支持 Windows**: 依赖 LibreHardwareMonitor DLL
- **需要 Conda**: 默认使用 `agent` 环境
- **防火墙**: 首次使用需允许 8000/8501 端口

## 📄 许可证

MIT License

---

> "一切正常。太无聊了，我去测算模拟宇宙。" —— 黑塔
