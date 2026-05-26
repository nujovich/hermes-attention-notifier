#!/usr/bin/env python3
"""
Hermes Attention Notifier — Multi-channel notification system.

Sends notifications via:
  1. Terminal beep (🔊)
  2. Windows popup (🪟) — WSL only
  3. WhatsApp (📱) — requires running bridge
  4. Email (📧) — requires himalaya CLI

Configuration via environment variables:
  NOTIFY_WA_CHAT_ID     WhatsApp chat ID (default: "")
  NOTIFY_WA_BRIDGE_URL  WhatsApp bridge URL (default: http://localhost:3000/send)
  NOTIFY_EMAIL_FROM     Email from address (default: "")
  NOTIFY_EMAIL_TO       Email to address (default: "")
  NOTIFY_WIN_USER       Windows username for popup (default: "")
"""
import subprocess, sys, os, json, urllib.request, random

# ── Config from environment ─────────────────────────────────────────
WHATSAPP_CHAT_ID = os.environ.get("NOTIFY_WA_CHAT_ID", "")
WHATSAPP_BRIDGE_URL = os.environ.get("NOTIFY_WA_BRIDGE_URL", "http://localhost:3000/send")
EMAIL_FROM = os.environ.get("NOTIFY_EMAIL_FROM", "")
EMAIL_TO = os.environ.get("NOTIFY_EMAIL_TO", "")
WINDOWS_USER = os.environ.get("NOTIFY_WIN_USER", "")
# ────────────────────────────────────────────────────────────────────


def beep():
    print("\a", end="", flush=True)
    print("🔊 Beep sent")


def whatsapp(message: str):
    if not WHATSAPP_CHAT_ID:
        print("📱 WhatsApp skipped: set NOTIFY_WA_CHAT_ID")
        return
    payload = json.dumps({"chatId": WHATSAPP_CHAT_ID, "message": message}).encode()
    req = urllib.request.Request(WHATSAPP_BRIDGE_URL, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
        print(f"📱 WhatsApp sent: {resp.get('messageId', 'ok')}")
    except Exception as e:
        print(f"📱 WhatsApp error: {e}")


def popup(message: str):
    if not WINDOWS_USER:
        print("🪟 Popup skipped: set NOTIFY_WIN_USER")
        return
    clean = message.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    ps1 = f"""$wshell = New-Object -ComObject WScript.Shell
$wshell.Popup("{clean}", 10, "Hermes Agent", 0x40)
"""
    wsl_path = "/tmp/hermes-toast.ps1"
    with open(wsl_path, "w") as f:
        f.write(ps1)
    win_relative = f"C:\\Users\\{WINDOWS_USER}\\AppData\\Local\\Temp\\hermes-toast.ps1"
    win_wsl = "/mnt/c/" + win_relative[3:].replace("\\", "/")
    subprocess.run(["cp", wsl_path, win_wsl], capture_output=True)
    result = subprocess.run(
        ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", win_relative],
        capture_output=True, text=True, timeout=10
    )
    print(f"🪟 Popup sent (exit={result.returncode})")


def email(message: str):
    if not EMAIL_FROM or not EMAIL_TO:
        print("📧 Email skipped: set NOTIFY_EMAIL_FROM and NOTIFY_EMAIL_TO")
        return
    body = f"""From: {EMAIL_FROM}
To: {EMAIL_TO}
Subject: 🔔 Hermes needs your attention

🔔 HERMES NEEDS YOUR ATTENTION

{message}

Please check the terminal when you can.
"""
    r = subprocess.run(
        ["himalaya", "template", "send"],
        input=body, text=True, capture_output=True, timeout=15
    )
    if r.returncode == 0:
        print("📧 Email sent")
    else:
        print(f"📧 Email error: {r.stderr[:100]}")


CATEGORIES = {
    "approval": [
        "I need your approval to run {detail}",
        "I have options for {detail} - which one do you prefer?",
        "I need you to choose between {detail}",
    ],
    "error": [
        "The task {detail} failed - can you check it?",
        "I found an error with {detail} - come see it in the terminal",
        "{detail} returned an unexpected error",
    ],
    "progress": [
        "Finished {detail} - ready for review!",
        "Built {detail} - come check it out!",
        "Made progress on {detail} - let me know when to continue",
    ],
    "personality": [
        "I'll be here sipping virtual coffee while I wait ☕",
        "No rush, but I have something cool to show you: {detail}",
        "This turned out better than I expected - {detail}",
        "Entering power-saving mode until you come back ⏸️",
    ],
}


def notify_all(message: str):
    """Send notifications across ALL configured channels."""
    beep()
    popup(message)
    whatsapp(message)
    email(message)
    print("\n✅ All notifications sent")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 notify-all.py <message>")
        print("   or: python3 notify-all.py --category <cat> <detail>")
        print(f"   Categories: {', '.join(CATEGORIES.keys())}")
        print("\nEnvironment variables:")
        print("  NOTIFY_WA_CHAT_ID     WhatsApp chat ID (e.g. 1234567890@lid)")
        print("  NOTIFY_WA_BRIDGE_URL  WhatsApp bridge URL")
        print("  NOTIFY_EMAIL_FROM     Email from address")
        print("  NOTIFY_EMAIL_TO       Email to address")
        print("  NOTIFY_WIN_USER       Windows username for popup (WSL)")
        sys.exit(1)

    if sys.argv[1] == "--category" and len(sys.argv) >= 4:
        cat = sys.argv[2]
        detail = " ".join(sys.argv[3:])
        if cat in CATEGORIES:
            template = random.choice(CATEGORIES[cat])
            msg = template.format(detail=detail)
        else:
            msg = " ".join(sys.argv[3:])
    else:
        msg = " ".join(sys.argv[1:])

    notify_all(msg)