# Weixin + Telegram Hermes Gateway setup notes

These notes capture a reusable setup pattern, not one-off credentials. Do not copy account IDs, tokens, QR state URLs, or home channel IDs into future replies.

## Context

A Hermes Gateway messaging setup session configured Weixin/WeChat first, then began Telegram setup.

The official `hermes-agent` skill had been loaded and confirmed that Hermes Gateway supports messaging platforms through official adapters and env-var configuration.

## Weixin / WeChat pattern

The user wanted Weixin configured. Hermes already included the official Weixin adapter and CLI setup logic:

- Adapter: `gateway/platforms/weixin.py`
- CLI setup/status logic: `hermes_cli/gateway.py` and `hermes_cli/setup.py`
- Config destination: `~/.hermes/.env`

The normal official path is `hermes gateway setup`, but it is interactive and QR-login based. In a tool/API environment, that can be awkward because the QR must be shown while a polling process waits.

A useful workaround is to split the official QR flow into two temporary helpers:

1. QR start helper
   - Calls the same Hermes Weixin QR/login API path used by setup.
   - Saves short-lived QR state under the Hermes home, e.g. `~/.hermes/weixin/qr_setup_state.json`.
   - Prints a QR URL or renders it as ASCII for the user.
2. QR poll helper
   - Reads the saved QR state.
   - Polls the official QR status endpoint until confirmed.
   - Writes the returned official env vars to `~/.hermes/.env`.
   - Sets safe default policies and home channel.

After confirmation, verify with:

```bash
hermes status --all
hermes gateway status
tail -80 ~/.hermes/logs/gateway.log
```

Do not stop at `.env` writes. The durable proof is adapter connection plus actual send/receive logs, e.g. gateway logs showing:

- `Connecting to weixin...`
- `✓ weixin connected`
- inbound message from Weixin
- response ready
- sending response

Safe defaults from the session:

- DM policy: `pairing`
- Allow all users: false
- Group policy: mention-only or disabled unless explicitly requested
- Home channel: set from the login result, but redact it in replies

## Telegram pattern

Telegram setup is simpler but needs a BotFather token.

Required/important env vars:

- `TELEGRAM_BOT_TOKEN` — required, from `@BotFather`.
- `TELEGRAM_ALLOWED_USERS` — comma-separated numeric Telegram user IDs; use it to avoid open access.
- `TELEGRAM_HOME_CHANNEL` — for cron/notification delivery; for a DM, this is usually the same numeric user ID.

If `TELEGRAM_ALLOWED_USERS` exists but `TELEGRAM_BOT_TOKEN` is missing, Telegram is not configured. Ask the user for the BotFather token, write it to `.env`, set home channel, restart gateway, and verify.

Never display the token. When checking token validity through Telegram `getMe`, keep output to bot metadata only and redact the token itself.

## Reporting style

When reporting status, separate:

- configured vs not configured
- gateway running vs stopped
- manual `hermes gateway run` vs installed service
- verified real message flow vs only configuration present

If a temporary setup process was intentionally killed and exits with `-15`, explain it briefly as expected cleanup rather than treating it as failure.
