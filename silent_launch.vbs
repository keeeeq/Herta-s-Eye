' 黑塔之眼 - 静默启动器 (需要管理员权限)
' 会自动请求 UAC 提权

Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 获取脚本所在目录
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' 以管理员身份运行 Python
objShell.ShellExecute "pythonw.exe", """" & strPath & "\tray_manager.py""", strPath, "runas", 0

Set objShell = Nothing
Set objFSO = Nothing
