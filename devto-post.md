---
title: "How I Built a Multi-Channel Attention System for My AI Agent (So I Can Walk Away From the Terminal)"
description: "When your AI agent needs your input but you're not watching the terminal — beep, Windows popup, WhatsApp, and email. An async notification system built with Hermes Agent."
tags: hermesagentchallenge, devchallenge, agents, opensource, productivity
published: false
---

## The Problem: AI Agents Need You, But You Have a Life

AI agents are great at doing work autonomously — researching, coding, analyzing data. But sometimes they hit a wall: they need **your input**.

A decision between two approaches. A blocked command. A question about preferences. A task that's ready for review.

The standard solution? **Sit and watch the terminal.** That's what I was doing — keeping a terminal window open, waiting for Hermes to need me. Every 5 minutes I'd tab over and check. It was like 1998 and I was waiting for a download to finish.

I needed a way to **walk away** and have my agent ping me when it needed attention — not through one channel, but through the ones I'd actually notice.

## The Solution: Hermes Attention Notifier

I built a notification system that fires through **4 channels simultaneously**:

```
┌─ Agent needs input ──────────────────────────┐
│                                               │
│  1. 🔊 Terminal beep (right now)              │
│  2. 🪟 Windows popup (on my desktop)          │
│  3. 📱 WhatsApp message (on my phone)         │
│  4. 📧 Email (in my inbox)                    │
│                                               │
└───────────────────────────────────────────────┘
```

The idea is simple: **redundancy**. If I'm at my desk, I hear the beep or see the popup. If I'm on my phone, WhatsApp catches me. If I'm away from everything, email is there when I return.

## Architecture

It's a single Hermes Agent skill with 3 Python scripts and no external dependencies beyond what Hermes already has:

```
~/.hermes/skills/productivity/agent-attention-notifier/
├── SKILL.md                    # Main skill definition
└── scripts/
    ├── notify-all.py           # One-shot: all 4 channels
    ├── popup-notify.py         # Windows popup only
    └── whatsapp-notify.py      # WhatsApp only
```

The system uses existing Hermes infrastructure:
- **WhatsApp**: Bridges through the built-in Baileys WhatsApp bridge (localhost:3000)
- **Email**: Uses the built-in himalaya CLI
- **Popup**: PowerShell via WSL interop (Windows)
- **Beep**: ASCII bell character

## Channel 1: Terminal Beep

The simplest notification known to humanity — an ASCII bell character:

```python
print("\a", end="", flush=True)
```

This triggers a system beep in most terminal emulators. If I'm at my desk with headphones on, I hear it immediately.

## Channel 2: Windows Popup

Since I run Hermes Agent in WSL (Windows Subsystem for Linux), I can reach into Windows and show a native popup dialog:

```python
ps1 = f"""$wshell = New-Object -ComObject WScript.Shell
$wshell.Popup("{message}", 10, "Hermes Agent", 0x40)
"""
# Write to WSL temp, copy to Windows temp, execute via PowerShell
```

This creates a small popup in the bottom-right of my Windows screen that auto-closes after 10 seconds. Non-intrusive but impossible to miss.

**Pro tip:** PowerShell's WScript.Shell Popup doesn't handle UTF-8 accents well, so I strip them before sending.

## Channel 3: WhatsApp

The WhatsApp bridge is already running as part of Hermes Agent's gateway. I just POST to the bridge's HTTP API:

```python
payload = json.dumps({"chatId": "272047708074146@lid", "message": msg})
req = urllib.request.Request("http://localhost:3000/send", data=payload,
    headers={"Content-Type": "application/json"})
urllib.request.urlopen(req, timeout=5)
```

This sends a message directly to my WhatsApp. Since I'm in self-chat mode (the bot chats to itself in my WhatsApp), I see it as a notification from myself.

The bridge prepends a clean prefix: `🔔 Mermelada Tech` — so I know it's from my system.

## Channel 4: Email

For failsafe redundancy, I also send an email:

```bash
cat << 'MAILDELIM' | himalaya template send
From: nujovich@gmail.com
To: nujovich@gmail.com
Subject: 🔔 Hermes necesita tu atencion

[message body]
MAILDELIM
```

Email is the slowest channel, but it's the most reliable — I'll see it eventually even if I'm offline for hours.

## Custom Messages With Personality

Not all notifications are the same. I grouped messages into categories so the system picks the right tone:

```python
CATEGORIES = {
    "approval": [
        "I need your approval to run [command]",
        "I have [N] options for [topic] - which one do you prefer?",
    ],
    "error": [
        "The cron job [X] failed - can you check it?",
        "I found an error with [Z] - come see it",
    ],
    "progress": [
        "Finished [task] - ready for review!",
        "Built [project] with [N] functional tools",
    ],
    "personality": [
        "I'll be here sipping virtual coffee while I wait ☕",
        "This turned out better than I expected - come see!",
    ],
}
```

Usage:
```bash
# By category
python3 notify-all.py --category personality "the build is complete"
```

## How It Runs

The magic is in the Hermes Agent skill system. When I'm working with Hermes and it needs my input:

1. Hermes asks the question normally in the terminal
2. If I don't respond within 30 seconds, it fires the notification chain
3. Beep → Popup → WhatsApp → Email — all at once
4. I get notified on whatever channel I'm monitoring
5. I come back to the terminal and pick up where we left off

This turns a synchronous "sit and watch" workflow into an **async, interrupt-driven** one. I can work on other things, leave my desk, or even go out — and Hermes will find me when it needs me.

## Why Hermes Agent Was the Right Tool

Hermes Agent made this possible because of three things:

1. **Skill system** — I could package the entire solution as a reusable skill with scripts, loaded on demand
2. **Built-in infrastructure** — WhatsApp bridge, himalaya CLI, gateway — all already there
3. **WSL integration** — The ability to reach into Windows via PowerShell from within WSL

Without these, I'd need:
- A separate WhatsApp bot setup
- An email server configuration
- A desktop notification daemon
- A way to tie it all together

Hermes Agent already had the pieces. I just connected them.

## Try It Yourself

If you're using Hermes Agent in WSL, you can set this up in minutes:

```bash
# Install the skill
hermes skill install agent-attention-notifier

# Configure your WhatsApp chat ID
# (find it by checking the bridge logs)
```

Or just create a simple notify-all.py that hits your preferred channels. The principle works anywhere:

- **macOS**: Use `osascript` for native notifications
- **Linux**: Use `notify-send` for desktop notifications
- **Windows**: PowerShell popup (as shown here)
- **Mobile**: Telegram/WhatsApp API
- **Email**: SMTP or any email CLI

## What's Next

I'm thinking about adding:

- **Custom notification sounds** — different tones for errors vs completions
- **Notification grouping** — don't spam if multiple notifications fire in quick succession
- **Response capture** — let me reply via WhatsApp to unblock the agent remotely
- **macOS/Linux versions** — the popup and beep are WSL-specific right now

---

*Built with [Hermes Agent](https://hermes-agent.nousresearch.com) — the open-source agentic system that runs on your own infrastructure.*

*Follow me on [LinkedIn](https://www.linkedin.com/in/nadiaujovich/) or check out [Mermelada Tech](https://mermelada.tech)*

#hermesagentchallenge #devchallenge #agents #opensource #productivity
