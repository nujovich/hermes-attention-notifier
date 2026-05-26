#!/usr/bin/env python3
"""Send a WhatsApp message via the local Baileys bridge.

Configure via env vars:
  NOTIFY_WA_CHAT_ID     WhatsApp chat ID (e.g. 1234567890@lid)
  NOTIFY_WA_BRIDGE_URL  Bridge URL (default: http://localhost:3000/send)
"""
import json, urllib.request, sys, os

def notify(message: str):
    chat_id = os.environ.get("NOTIFY_WA_CHAT_ID", "")
    if not chat_id:
        print("Set NOTIFY_WA_CHAT_ID to enable WhatsApp notifications")
        sys.exit(1)
    bridge_url = os.environ.get("NOTIFY_WA_BRIDGE_URL", "http://localhost:3000/send")
    payload = json.dumps({"chatId": chat_id, "message": message}).encode()
    req = urllib.request.Request(bridge_url, data=payload,
        headers={"Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
        print(f"WhatsApp sent: {resp.get('messageId', 'ok')}")
    except Exception as e:
        print(f"WhatsApp error: {e}")

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "Hermes needs your attention"
    notify(msg)