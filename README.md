# Agent Attention Notifier

Multi-channel notification system for Hermes Agent. When the agent needs your input and you're not at the terminal, it will ping you through 4 channels simultaneously.

## Channels

| Channel | How | When you'll notice |
|---------|-----|-------------------|
| 🔊 Beep | ASCII bell (`\a`) | At your desk with headphones |
| 🪟 Popup | PowerShell WScript.Popup (Windows) | Looking at your screen |
| 📱 WhatsApp | Baileys bridge API | On your phone |
| 📧 Email | himalaya CLI | In your inbox |

## Installation

```bash
# Via Hermes skill manager
hermes skill install https://github.com/nujovich/hermes-attention-notifier
```

Then add to your `~/.hermes/config.yaml` or load via `/skill agent-attention-notifier` in a session.

## Usage

```bash
# All 4 channels with a custom message
python3 scripts/notify-all.py "Termine la tarea - veni a ver"

# Or by category (random message from template)
python3 scripts/notify-all.py --categoria personalidad "el build se completo"

# Individual channels
python3 scripts/popup-notify.py "Tu atencion es requerida"
python3 scripts/whatsapp-notify.py "Revisa el terminal cuando puedas"
```

## Categories

- `approval` — Approval/decision needed
- `error` — Something failed
- `progress` — Task completed
- `personality` — Fun, casual messages

## Requirements

- Hermes Agent with WhatsApp bridge enabled (for WhatsApp channel)
- himalaya CLI configured (for email channel)
- WSL with PowerShell access (for Windows popup)
- Linux with `notify-send` (for popup on Linux — modify popup-notify.py)

## Customization

Edit the constants at the top of `scripts/notify-all.py`:

```python
WHATSAPP_CHAT_ID = "your_chat_id@lid"
EMAIL_FROM = "your@email.com"
EMAIL_TO = "your@email.com"
WINDOWS_USER = "YourWindowsUsername"
```

## License

MIT — part of the Hermes Agent Challenge.
