' 黑塔之眼 - 静默启动器 (v3.0 Final)
' 使用 ShellExecute "runas" (管理员) + 0 (隐藏窗口) 启动

Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' 构造命令: 切换目录 -> 激活 conda -> 启动管理脚本
' 注意: 使用 python.exe 即可，因为父 CMD 窗口本身是隐藏的
strCmd = "/c cd /d """ & strPath & """ && call conda activate agent && python tray_manager.py"

' 执行命令
' "runas": 请求管理员权限 (UAC)
' 0: 隐藏窗口 (SW_HIDE)
objShell.ShellExecute "cmd.exe", strCmd, "", "runas", 0

Set objShell = Nothing
Set objFSO = Nothing
