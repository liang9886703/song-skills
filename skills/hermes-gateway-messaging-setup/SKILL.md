---
name: hermes-gateway-messaging-setup
description: Configure and verify Hermes Gateway messaging channels such as Weixin/WeChat and Telegram using the official Hermes adapters, with safe secret handling and real end-to-end verification.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, gateway, messaging, telegram, weixin, setup, verification]
    related_skills: [hermes-agent]
---

# Hermes Gateway Messaging Setup

Use this skill when the user asks to configure, inspect, troubleshoot, or verify Hermes Agent messaging channels: Weixin/WeChat, Telegram, Discord, Slack, Feishu, WeCom, etc.

This is a local procedural overlay for channel setup. Load the official `hermes-agent` skill first whenever working on Hermes itself; then use this skill for the practical gateway/channel workflow and verification checklist.

## Core principles

1. Use official Hermes Gateway adapters whenever available.
   - Do not invent a parallel bot runner unless the user explicitly asks for a custom integration.
   - For Weixin/WeChat, Hermes has an official adapter in `gateway/platforms/weixin.py`.
   - For Telegram, Hermes reads official env vars such as `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, and `TELEGRAM_HOME_CHANNEL`.
2. Treat `.env`, QR login state files, bot tokens, account IDs, and home channel IDs as sensitive.
   - Write secrets to `~/.hermes/.env` only.
   - Never echo raw tokens or API keys in the final reply.
   - Redact tokens and credential-like strings in status excerpts.
3. Verify with real runtime output, not just config writes.
   - `hermes status --all` should show the platform as configured.
   - `hermes gateway status` should show the gateway running.
   - Gateway logs should show the adapter connected.
   - When possible, confirm an actual inbound message and outbound response.
4. Distinguish config success from service durability.
   - `hermes gateway run` starts a manual process.
   - `hermes gateway install` + `hermes gateway start` installs/starts the managed service.
   - Tell the user which mode is currently running.

## Standard workflow

1. Load context.
   - Load `hermes-agent` first.
   - Check `hermes config path`, `hermes config env-path`, `hermes status --all`, and `hermes gateway status`.
2. Identify required env vars for the target platform.
   - Prefer Hermes CLI docs/code/status output over guessing.
   - For Telegram: `TELEGRAM_BOT_TOKEN` is required; `TELEGRAM_ALLOWED_USERS` restricts access; `TELEGRAM_HOME_CHANNEL` is used for cron/notification delivery.
   - For Weixin: `WEIXIN_ACCOUNT_ID`, `WEIXIN_TOKEN`, `WEIXIN_BASE_URL`, `WEIXIN_CDN_BASE_URL`, and optional policy/home vars are used by the official adapter.
3. Configure using official setup where practical.
   - Preferred: `hermes gateway setup`.
   - If the environment cannot support a long interactive QR/token prompt, use small temporary scripts that call the same Hermes setup/login functions and only write official env vars.
4. Restart or start the gateway.
   - If editing `.env`, restart the gateway or start a fresh `hermes gateway run` so env changes are loaded.
   - Avoid assuming a running gateway picked up new env vars.
5. Verify.
   - Run `hermes status --all` and inspect the Messaging Platforms section.
   - Run `hermes gateway status`.
   - Inspect `~/.hermes/logs/gateway.log` for adapter connection lines and send/receive evidence.
   - Ask the user to send a message to the bot/channel if end-to-end proof is needed.

## Weixin / WeChat notes

Hermes supports Weixin through its official adapter and Tencent iLink QR login. If the interactive setup flow is hard to drive from an API/tool environment, split the flow:

1. Generate a QR login URL/state by calling the official Weixin QR login API helper or the same endpoints used by Hermes setup.
2. Show the QR link or render it as ASCII for the user to scan.
3. Run a polling helper that waits for confirmation.
4. On confirmation, write only official env vars to `~/.hermes/.env`.
5. Start/restart gateway and verify the official adapter connects.

Safe defaults used in the session that produced this skill:

- DM policy: `pairing`, not open access.
- Group policy: mention-only or disabled unless the user explicitly wants group responses.
- Home channel: set from the confirmed login/user result, but do not expose it unnecessarily.

## Telegram notes

Telegram requires user-provided BotFather credentials.

1. Ask the user to create a bot via `@BotFather` and provide the bot token.
2. Write `TELEGRAM_BOT_TOKEN` to `.env` without displaying it.
3. Set `TELEGRAM_ALLOWED_USERS` to the user's numeric Telegram ID if known; otherwise ask them to message `@userinfobot`.
4. Set `TELEGRAM_HOME_CHANNEL` to the same user ID for DM delivery, unless they want a different chat/channel.
5. Restart gateway and verify Telegram shows configured.
6. Ask the user to message the bot and confirm an actual response.

## Verification snippets

Use commands like these, with redaction when presenting output:

```bash
hermes gateway status
hermes status --all
```

For logs:

```bash
tail -80 ~/.hermes/logs/gateway.log
```

Look for lines such as:

- `Connecting to <platform>...`
- `✓ <platform> connected`
- `Gateway running with N platform(s)`
- inbound message logs
- response ready / sending response logs

## Pitfalls

- A killed temporary setup process with exit code `-15` may be expected if it was manually terminated after switching to a better setup path. Do not report it as a channel failure without checking the active gateway and final platform status.
- `hermes status --all` can show configured while the gateway is still stopped. Always check both config status and gateway runtime status.
- Updating `.env` does not prove the channel works. Require adapter connection logs or an actual send/receive test before declaring completion.
- Avoid exposing token-like values from `hermes status --all`; redact before quoting.
- Discord can be "connected" while no agent turn starts. Diagnose in this order: look for `inbound message: platform=discord` and `[Discord] Flushing text batch` in `~/.hermes/logs/gateway.log`; check `DISCORD_ALLOWED_USERS`/roles against the sender; check `DISCORD_REQUIRE_MENTION`, `DISCORD_FREE_RESPONSE_CHANNELS`, and `DISCORD_ALLOWED_CHANNELS`; verify the bot is in the guild and can see the target channel; and confirm Discord Developer Portal privileged intents (especially Message Content Intent, plus Server Members Intent when username/role allowlists are used). Remember Hermes does not keep a separate per-channel agent process idle — the AIAgent is created for an inbound event after adapter filters pass.

## References

- `references/weixin-telegram-session-setup.md` — concise notes from the session where Weixin was configured via split QR helpers and Telegram setup prerequisites were identified.
