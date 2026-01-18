' 黑塔之眼 - 静默启动器 (使用 Conda agent 环境)
' 会自动请求 UAC 提权

Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 获取脚本所在目录
strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' 通过 cmd 激活 conda 环境后运行 (以管理员身份)
strCmd = "/c cd /d """ & strPath & """ && conda activate agent && pythonw tray_manager.py"
objShell.ShellExecute "cmd.exe", strCmd, strPath, "runas", 0

Set objShell = Nothing
Set objFSO = Nothing
