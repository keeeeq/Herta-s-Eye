' 黑塔之眼 - 静默启动器 (v3.0 Final)
' 使用 ShellExecute "runas" (管理员) + 0 (隐藏窗口) 启动

Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

strPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' 构造命令: 切换目录 -> 启动管理脚本
' 默认使用系统 PATH 中的 python
' 如果使用虚拟环境，请修改此处 (例如: "call conda activate myenv && python ...")
strCmd = "/c cd /d """ & strPath & """ && python tray_manager.py"

' 执行命令
' "runas": 请求管理员权限 (UAC)
' 0: 隐藏窗口 (SW_HIDE)
objShell.ShellExecute "cmd.exe", strCmd, "", "runas", 0

Set objShell = Nothing
Set objFSO = Nothing
