# Telegram interface

The Telegram interface is an operator channel for the bounded Ambivikhry runtime.

## Security model

The bot fails closed unless `TELEGRAM_ALLOWED_USER_IDS` is configured. Only
those Telegram numeric user IDs can interact with the agent.

Each allowed Telegram user receives a separate runtime memory directory. The
Telegram layer does not bypass `PolicyGate`, `DryRunAdapter`, verification,
bounded iterations, or the existing audit log.

A request that looks like privilege expansion is reported separately to the
operator and is never approved by the bot.

## Environment

Required:

```text
TELEGRAM_BOT_TOKEN=...
TELEGRAM_ALLOWED_USER_IDS=123456789
AMBIVIKHRY_API_KEY=...
AMBIVIKHRY_MODEL=...
```

Optional:

```text
AMBIVIKHRY_BASE_URL=https://api.openai.com/v1
AMBIVIKHRY_WORKDIR=./runtime/telegram
AMBIVIKHRY_MAX_ITERATIONS=4
```

For multiple operators, comma-separate Telegram IDs:

```text
TELEGRAM_ALLOWED_USER_IDS=123456789,987654321
```

## Run locally

Install the package with the Telegram extra, then:

```bash
export TELEGRAM_BOT_TOKEN='...'
export TELEGRAM_ALLOWED_USER_IDS='123456789'
export AMBIVIKHRY_API_KEY='...'
export AMBIVIKHRY_MODEL='...'
python -m ambivikhry.telegram_bot
```

## Commands

- `/start`, `/help` — interface help
- `/status` — runtime state
- `/audit` — recent audit events
- `/reset` — discard the in-memory instance and start a clean one
- ordinary text — send a task to Ambivikhry

The bot uses long polling, so no public HTTP endpoint is required for the
first deployment. For production, keep the token and model credentials in
the host's secret manager rather than committing them to the repository.
