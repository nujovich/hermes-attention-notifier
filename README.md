<div align="center">
  <img src="https://raw.githubusercontent.com/NousResearch/hermes-agent/HEAD/assets/banner.png" alt="Hermes Agent" width="600"/>
  <br/><br/>
  <h1>Agent Attention Notifier 📣</h1>
  <p><strong>Powered by <a href="https://hermes-agent.nousresearch.com">Hermes Agent</a></strong></p>
  <p><em>Multi-channel notification system for Hermes Agent. When the agent needs your input and you're not at the terminal, it will ping you through 4 channels simultaneously.</em></p>
  <br/>
  <p>
    <a href="https://dev.to/nujovich/building-an-autonomous-mcp-lead-generation-system-with-hermes-agent">
      <img src="https://img.shields.io/badge/DEV.to-Hermes%20Challenge-673773?style=for-the-badge&logo=dev.to" alt="Dev.to Post"/>
    </a>
    <a href="https://hermes-agent.nousresearch.com">
      <img src="https://img.shields.io/badge/Hermes%20Agent-Docs-FFD700?style=for-the-badge" alt="Hermes Agent Docs"/>
    </a>
    <a href="https://nadiaujovich.dev">
      <img src="https://img.shields.io/badge/By-Nadia%20Ujovich-0D7377?style=for-the-badge" alt="Nadia Ujovich"/>
    </a>
  </p>
</div>

---

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
python3 scripts/notify-all.py "I finish the task. Come and see! 😶"

# Or by category (random message from template)
python3 scripts/notify-all.py --categoria personalidad "The build has completed 😊"

# Individual channels
python3 scripts/popup-notify.py "Your attention is required 😁"
python3 scripts/whatsapp-notify.py "Check this when you have time 🤸"
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

MIT — Built with [Hermes Agent](https://hermes-agent.nousresearch.com) by [Nadia Ujovich](https://nadiaujovich.dev)

<div align="center">
  <br/>
  <sub>Part of the <a href="https://dev.to/devteam/join-the-hermes-agent-challenge-1000-in-prizes-13cd">Hermes Agent Challenge</a> · May 2026</sub>
</div>

