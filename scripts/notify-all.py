#!/usr/bin/env python3
"""
Hermes Attention Notifier — Multi-channel notification system.

Sends notifications via:
  1. Terminal beep (🔊)
  2. Windows popup (🪟)
  3. WhatsApp (📱)
  4. Email (📧)
"""
import subprocess, sys, os, json, urllib.request

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Config ──────────────────────────────────────────────────────────
WHATSAPP_CHAT_ID = "272047708074146@lid"
WHATSAPP_BRIDGE_URL = "http://localhost:3000/send"
EMAIL_FROM = "nujovich@gmail.com"
EMAIL_TO = "nujovich@gmail.com"
WINDOWS_USER = "NadiaUjovich"
# ────────────────────────────────────────────────────────────────────


def beep():
    print("\a", end="", flush=True)
    print("🔊 Beep sent")


def whatsapp(message: str):
    payload = json.dumps({"chatId": WHATSAPP_CHAT_ID, "message": message}).encode()
    req = urllib.request.Request(WHATSAPP_BRIDGE_URL, data=payload,
        headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
    print(f"📱 WhatsApp sent: {resp.get('messageId', 'ok')}")


def popup(message: str):
    clean = message.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    ps1 = f"""$wshell = New-Object -ComObject WScript.Shell
$wshell.Popup("{clean}", 10, "Hermes Agent", 0x40)
"""
    wsl_path = "/tmp/hermes-toast.ps1"
    with open(wsl_path, "w") as f:
        f.write(ps1)
    win_relative = "C:\\Users\\{}\\AppData\\Local\\Temp\\hermes-toast.ps1".format(WINDOWS_USER)
    win_wsl = "/mnt/c/" + win_relative[3:].replace("\\", "/")
    subprocess.run(["cp", wsl_path, win_wsl], capture_output=True)
    result = subprocess.run(
        ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", win_relative],
        capture_output=True, text=True, timeout=10
    )
    print(f"🪟 Popup sent (exit={result.returncode})")


def email(message: str):
    body = f"""From: {EMAIL_FROM}
To: {EMAIL_TO}
Subject: 🔔 Hermes necesita tu atencion

🔔 HERMES NECESITA TU ATENCION

{message}

Por favor revisa el terminal cuando puedas.
"""
    r = subprocess.run(
        ["himalaya", "template", "send"],
        input=body, text=True, capture_output=True, timeout=15
    )
    if r.returncode == 0:
        print("📧 Email sent")
    else:
        print(f"📧 Email error: {r.stderr[:100]}")


def notify_all(message: str):
    """Send notifications across ALL channels."""
    beep()
    popup(message)
    whatsapp(message)
    email(message)
    print("\n✅ Notificación completa — todos los canales enviados")


CATEGORIES = {
    "approval": [
        "I need your approval to run {detail}",
        "I have {detail} options for {topic} - which one do you prefer?",
        "I need you to choose between {detail}",
    ],
    "error": [
        "The cron job {detail} failed - can you check it?",
        "I found an error with {detail} - come see it in the terminal",
        "{detail} returned an unexpected error",
    ],
    "progress": [
        "Finished {detail} - ready for review!",
        "Built {detail} - come check it out!",
        "Made progress on {detail} - let me know when you want to continue",
    ],
    "personality": [
        "I'll be here sipping virtual coffee while I wait ☕",
        "No rush, but I have something cool to show you: {detail}",
        "This turned out better than I expected - {detail}",
        "Entering power-saving mode until you come back ⏸️",
    ],
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 notify-all.py <mensaje>")
        print("   o: python3 notify-all.py --category <cat> <detail>")
        print(f"   Categories: {', '.join(CATEGORIES.keys())}")
        sys.exit(1)

    if sys.argv[1] == "--category" and len(sys.argv) >= 4:
        cat = sys.argv[2]
        detail = " ".join(sys.argv[3:])
        if cat in CATEGORIES:
            import random
            template = random.choice(CATEGORIES[cat])
            msg = template.format(detail=detail)
        else:
            msg = " ".join(sys.argv[3:])
    else:
        msg = " ".join(sys.argv[1:])

    notify_all(msg)