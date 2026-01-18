@echo off
cd /d "%~dp0"

:: --- AUTO ADMIN ELEVATION ---
NET SESSION >nul 2>&1
if %errorLevel% NEQ 0 (
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit
)

:: --- KILL OLD PROCESSES ---
taskkill /F /IM python.exe >nul 2>&1

:: --- ACTIVATE CONDA ---
call conda activate agent

:: --- START TRAY MANAGER ---
echo 启动黑塔之眼...
python tray_manager.py
