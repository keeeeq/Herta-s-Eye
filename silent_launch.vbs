Set WshShell = CreateObject("WScript.Shell")
' 使用 cmd 激活 conda 环境后运行
WshShell.Run "cmd /c ""cd /d e:\Herta-s-Eye && conda activate agent && pythonw tray_manager.py""", 0
Set WshShell = Nothing
