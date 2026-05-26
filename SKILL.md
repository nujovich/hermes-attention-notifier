---
name: agent-attention-notifier
description: Notify the user via beep, Windows popup, WhatsApp, and email when the agent needs attention.
---

# Agent Attention Notifier

When the agent needs user input (clarify times out, command blocked, waiting >30s), notify through all configured channels.

## Channels

| Channel | Config | Platform |
|---------|--------|----------|
| 🔊 Beep | None (built-in) | Any terminal |
| 🪟 Popup | `NOTIFY_WIN_USER` | Windows (WSL) |
| 📱 WhatsApp | `NOTIFY_WA_CHAT_ID` | Any (requires Baileys bridge) |
| 📧 Email | `NOTIFY_EMAIL_FROM`, `NOTIFY_EMAIL_TO` | Any (requires himalaya) |

## Setup

```bash
# Clone the repo
git clone https://github.com/nujovich/hermes-attention-notifier.git ~/.hermes/skills/productivity/agent-attention-notifier

# Or install via Hermes skill manager
hermes skill install https://github.com/nujovich/hermes-attention-notifier
```

Set environment variables in `~/.hermes/.env` or `~/.hermes/profiles/<profile>/.env`:

```bash
# WhatsApp
NOTIFY_WA_CHAT_ID="272047708074146@lid"
NOTIFY_WA_BRIDGE_URL="http://localhost:3000/send"

# Email
NOTIFY_EMAIL_FROM="you@gmail.com"
NOTIFY_EMAIL_TO="you@gmail.com"

# Windows popup (WSL only)
NOTIFY_WIN_USER="YourWindowsUsername"
```

## Usage

```bash
# All channels with a custom message
python3 scripts/notify-all.py "Task finished - ready for review"

# By category (random message)
python3 scripts/notify-all.py --category personality "the build is complete"

# Individual channels
python3 scripts/popup-notify.py "Check the terminal"
python3 scripts/whatsapp-notify.py "I need your input"
```

## Categories

| Category | Tone | Example |
|----------|------|---------|
| `approval` | Professional | "I need your approval to run [command]" |
| `error` | Urgent | "[X] failed - can you check it?" |
| `progress` | Positive | "Finished [task] - ready for review!" |
| `personality` | Casual | "Sipping virtual coffee while I wait ☕" |

## How It Works

When triggered (e.g., clarify() times out), the agent:

1. Plays a terminal beep
2. Sends a Windows popup (if configured)
3. Sends a WhatsApp message (if configured)
4. Sends an email (if configured)

Each channel is optional — set only the env vars for the channels you want.

## Customization

Add your own message templates in `CATEGORIES` inside `scripts/notify-all.py`. Each category supports `{detail}` as a placeholder.

## Changelog

### v1.1 — 2026-05-26

- **Resilient multi-channel**: Each channel is wrapped in try/except — a failure in WhatsApp or popup no longer blocks email from being sent
- **Popup improvements**: Increased visibility duration 10s → 30s; added `msg *` fallback for Windows native dialog; fixed double-quote escaping in PowerShell
- **Bridge auto-recovery**: WhatsApp bridge restart detected and handled gracefully

## Requirements (per channel)

- **Beep**: Any terminal emulator
- **Popup**: WSL with PowerShell access to Windows
- **WhatsApp**: Running Hermes WhatsApp bridge (Baileys) on localhost:3000
- **Email**: Himalayan CLI configured (`himalaya --version`)

## License

MIT — part of the [Hermes Agent Challenge](https://dev.to/nujovich/building-an-autonomous-mcp-lead-generation-system-with-hermes-agent-gf4).