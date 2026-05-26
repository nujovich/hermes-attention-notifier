#!/usr/bin/env python3
"""Send a Windows popup notification via PowerShell (WSL only).

Configure via env var: NOTIFY_WIN_USER (Windows username).
"""
import subprocess, sys, os

def notify(message: str):
    user = os.environ.get("NOTIFY_WIN_USER", "")
    if not user:
        print("Set NOTIFY_WIN_USER to enable Windows popup")
        sys.exit(1)
    clean = message.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    ps1 = f"""$wshell = New-Object -ComObject WScript.Shell
$wshell.Popup("{clean}", 10, "Hermes Agent", 0x40)
"""
    wsl_path = "/tmp/hermes-toast.ps1"
    with open(wsl_path, "w") as f:
        f.write(ps1)
    win_relative = f"C:\\Users\\{user}\\AppData\\Local\\Temp\\hermes-toast.ps1"
    win_wsl = "/mnt/c/" + win_relative[3:].replace("\\", "/")
    subprocess.run(["cp", wsl_path, win_wsl], capture_output=True)
    result = subprocess.run(
        ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", win_relative],
        capture_output=True, text=True, timeout=10
    )
    print(f"Popup sent (exit={result.returncode})")

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "Hermes needs your attention"
    notify(msg)