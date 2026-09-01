---
name: messaging-channel-migration
description: "Migrate and verify Hermes/OpenClaw-style messaging gateway channels such as Telegram and Weixin without exposing secrets."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  created_by: agent
  tags: [hermes, gateway, messaging, telegram, weixin, openclaw, launchd]
---

# Messaging Channel Migration

Use this when configuring, migrating, or verifying messaging channels for Hermes Gateway, especially when the user says a channel was already configured in OpenClaw or another agent runtime.

This skill complements the protected `hermes-agent` skill. Load `hermes-agent` first for official commands, then use this skill for migration workflow, verification discipline, and session-specific pitfalls.

## Core principles

1. Treat all bot tokens, account IDs, API keys, QR tokens, and `.env` values as secrets.
   - Never print raw tokens.
   - Redact copied config in summaries.
   - It is okay to write secrets into the correct local `.env` when the user explicitly asks to configure/migrate.
2. Prefer official gateway adapters and CLI behavior.
   - Do not implement a new channel bridge unless the platform is unsupported.
   - Small helper scripts are acceptable only to automate official setup steps, e.g. QR login polling or config migration.
3. Always verify three layers before declaring success:
   - Config: `hermes status --all` shows the platform configured.
   - Runtime: gateway log shows the adapter connected.
   - Delivery: send or receive a real test message when possible.
4. If the user wants persistent gateway operation, install/start the official service instead of leaving `hermes gateway run` attached to a command-line session.

## Telegram migration from OpenClaw

When the user says Telegram is already configured in OpenClaw:

1. Inspect OpenClaw config paths, commonly:
   - `~/.openclaw/openclaw.json`
   - `~/.openclaw/openclaw.json.last-good`
   - timestamped backups if the current file lacks the token
2. Look for the Telegram account config, commonly:
   - `channels.telegram.accounts.<accountId>.botToken`
   - often accountId is `personal`
3. Copy into Hermes `.env`:
   - `TELEGRAM_BOT_TOKEN=<bot token>`
   - `TELEGRAM_ALLOWED_USERS=<numeric user id allowlist>`
   - `TELEGRAM_HOME_CHANNEL=<numeric user id or chat id>`
4. Use the Telegram API `getMe` to verify the token, but print only bot metadata, never the token.
5. Restart or start the gateway and confirm logs contain `telegram connected`.
6. Send a test message to `TELEGRAM_HOME_CHANNEL` or ask the user to message the bot to verify inbound handling.

## Weixin / WeChat setup pattern

Hermes has an official Weixin adapter. If the interactive setup flow is awkward in an agent API session:

1. Use official Hermes Weixin adapter/API helpers to generate the QR login URL.
2. Show the user an ASCII QR code or the QR URL.
3. Poll the official QR status endpoint until confirmed.
4. Save the returned account/token/base URLs/home channel into Hermes `.env`.
5. Start/restart gateway and verify logs show `weixin connected` and, if possible, a real inbound DM.

Do not describe this as a custom channel implementation. It is official Hermes support plus helper automation for setup ergonomics.

## Gateway service on macOS

If the gateway is running manually and the user asks to “启动 gateway” or make it persistent:

1. Check current status with `hermes gateway status`.
2. Install and start the launchd service:
   - `hermes gateway install`
   - `hermes gateway start`
3. Verify:
   - `hermes gateway status` shows a launchd plist and PID.
   - `hermes status --all` shows `Gateway Service` running with manager `launchd`.
   - Gateway logs show all configured platform adapters connected.
4. Report the LaunchAgent path, usually:
   - `~/Library/LaunchAgents/ai.hermes.gateway.plist`

## Pitfalls

- `hermes gateway restart` may stop a manually-run gateway and time out while ownership changes. Follow up with `hermes gateway status`; if stopped, run `hermes gateway run` temporarily or `hermes gateway install && hermes gateway start` for persistent service.
- Avoid using shell output that exposes `.env` contents. If you must inspect values, print presence, lengths, or redacted summaries.
- Do not store session-specific bot IDs or chat IDs in the skill. Put concrete details in references only if they are non-secret and useful as examples.

## References

- `references/hermes-openclaw-channel-migration.md` — concrete migration recipe from a session where Telegram was copied from OpenClaw and Weixin was set up through Hermes official QR login.
- `references/hermes-profile-model-switching.md` — safe cross-profile model/provider matching, endpoint verification, secret reuse, and gateway reload boundaries.
