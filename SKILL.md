---
name: agent-attention-notifier
description: Notify Nadia via WhatsApp + email when Hermes needs her attention or approval.
---

# Agent Attention Notifier

When the agent needs user input (clarify times out, terminal command blocked, or waiting more than 2 minutes for a response), notify Nadia through both channels.

## Triggers
- `clarify` tool times out without response
- Terminal command returns "BLOCKED: User denied this command"
- Waiting more than 30 seconds for user input after asking a question

## Sound Alert
```bash
echo -e '\a'
```

## Windows Toast Popup
```bash
python3 /home/nujovich/.hermes/skills/productivity/agent-attention-notifier/scripts/popup-notify.py "mensaje"
```

## WhatsApp Notification
```bash
python3 /home/nujovich/.hermes/skills/productivity/agent-attention-notifier/scripts/whatsapp-notify.py "mensaje"
```

## Email Notification
```bash
python3 /home/nujovich/.hermes/skills/productivity/agent-attention-notifier/scripts/notify-all.py "mensaje"
```

## One-shot: all channels
```bash
python3 /home/nujovich/.hermes/skills/productivity/agent-attention-notifier/scripts/notify-all.py "mensaje"
```

## Preference History
- May 26, 2026: Prefix changed from "🤖 Agente Financiero" to "🔔 Mermelada Tech" — user wanted cleaner, more generic WhatsApp prefix
- May 26, 2026: Dual notification (WhatsApp + email) requested — user not always at terminal

## Custom Messages by Category

Choose the most appropriate message based on context. Always keep them short.

### 🔧 Técnicos / Error
```
"Necesito tu aprobacion para ejecutar [comando]"
"El cron de [X] fallo - necesito que revises [Y]"
"Encontre un error con [Z] - ven a verlo al terminal"
"[Tool] devolvio un error inesperado - necesito tu opinion"
```

### 🤔 Decisión
```
"Tengo [N] opciones para [tema] - cual preferis?"
"Necesito que elijas entre [A] y [B]"
"No estoy seguro de como seguir con [X]"
"Hay [N] caminos posibles para [tema] - decidi cuando vuelvas"
```

### 📢 Progreso / Resultados
```
"Termine [tarea] - listo para revision!"
"Avance hasta [punto] - avisame cuando quieras seguir"
"Encontre algo interesante sobre [tema]"
"Construi [proyecto] con [N] tools funcionales - veni a ver"
"[Tarea] completada - resumen esperando en el terminal"
```

### 😄 Con personalidad (usar con moderación)
```
"Voy a esperar aqui tomando cafe virtual ☕"
"Sin prisa, pero cuando vuelvas tengo algo copado para mostrarte"
"Tarea completada con 🎉 - veni a ver el resultado"
"Me quedo aca en modo ahorro de energia hasta que vuelvas ⏸️"
"Esto quedo mejor de lo que esperaba - veni a ver!"
```

## Flow
1. First attempt normally (ask question / use clarify)
2. Determine message category based on context
3. If no response after 30s → beep + Windows popup + WhatsApp + email
4. Wait for user to return to terminal

## Notes
- Always send BOTH WhatsApp AND email so there's redundancy
- Keep messages short and clear - just enough context for Nadia to know what's needed
- Nadia prefers Spanish for all notifications
- WhatsApp bridge is at localhost:3000, financiero profile