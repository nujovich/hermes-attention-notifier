#!/usr/bin/env python3
"""Send a Windows popup notification via PowerShell."""
import subprocess, os, sys, tempfile

PS1_CONTENT = """$wshell = New-Object -ComObject WScript.Shell
$wshell.Popup("{message}", 30, "Hermes Agent", 0x40) | Out-Null
"""

def notify(message: str):
    # Clean accents for Windows encoding
    clean = message.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    ps1 = PS1_CONTENT.format(message=clean)

    # Write to WSL temp
    wsl_path = "/tmp/hermes-toast.ps1"
    with open(wsl_path, "w") as f:
        f.write(ps1)

    # Copy to Windows temp
    win_path = r"C:\Users\NadiaUjovich\AppData\Local\Temp\hermes-toast.ps1"
    win_wsl = "/mnt/c/" + win_path[3:].replace("\\", "/")
    subprocess.run(["cp", wsl_path, win_wsl], capture_output=True)

    # Execute via PowerShell (25s timeout: WSL↔Windows interop overhead)
    result = subprocess.run(
        ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", win_path],
        capture_output=True, timeout=25
    )
    print(f"Popup sent (exit={result.returncode})")

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "Hermes necesita tu atencion - revisa el terminal"
    notify(msg)