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
taskkill /F /IM streamlit.exe >nul 2>&1

:: --- ACTIVATE CONDA ---
call conda activate agent >nul 2>&1

:: --- START BACKEND (Completely Hidden) ---
powershell -WindowStyle Hidden -Command "Start-Process python -ArgumentList '-m backend.main' -WindowStyle Hidden"

:: --- WAIT ---
timeout /t 3 /nobreak >nul

:: --- START FRONTEND (Completely Hidden) ---
powershell -WindowStyle Hidden -Command "Start-Process streamlit -ArgumentList 'run frontend/app.py --server.address 0.0.0.0 --server.headless true' -WindowStyle Hidden"

:: --- WAIT ---
timeout /t 2 /nobreak >nul

:: --- SHOW BALLOON NOTIFICATION (Simpler, more reliable) ---
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $notify = New-Object System.Windows.Forms.NotifyIcon; $notify.Icon = [System.Drawing.SystemIcons]::Information; $notify.Visible = $true; $notify.BalloonTipTitle = '黑塔之眼'; $notify.BalloonTipText = '系统已启动 ✅ 手机访问: http://192.168.26.35:8501'; $notify.ShowBalloonTip(5000); Start-Sleep -Seconds 3; $notify.Dispose()"

exit
