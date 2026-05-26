#!/usr/bin/env python3
"""Send a WhatsApp notification via the local bridge API."""
import json, urllib.request, sys

CHAT_ID = "272047708074146@lid"
BRIDGE_URL = "http://localhost:3000/send"

def notify(message: str):
    payload = json.dumps({"chatId": CHAT_ID, "message": message}).encode()
    req = urllib.request.Request(BRIDGE_URL, data=payload,
        headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req, timeout=5)
    result = json.loads(resp.read())
    print(f"WhatsApp notification sent: {result.get('messageId', 'ok')}")

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) or "🔔 Hermes necesita tu atencion - revisa el terminal"
    notify(msg)