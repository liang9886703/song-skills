---
name: hermes-gateway-debugging
description: "Debug Hermes Gateway platform adapters and messaging delivery paths."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, gateway, messaging, debugging, platform-adapters]
    related_skills: [hermes-agent, systematic-debugging]
---

# Hermes Gateway Debugging

Use this skill when debugging Hermes messaging gateway issues: platform adapters, inbound/outbound delivery, media transfer, home-channel delivery, gateway restarts, or logs under `~/.hermes/logs/gateway.log`.

## Principles

1. **Start from the original source, not guesses.** Inspect gateway logs and the relevant adapter code before changing anything.
2. **Find the failing boundary.** Separate platform connection, long-poll/webhook intake, agent response generation, outbound text send, and media upload/download.
3. **Fix the boundary, not the symptom.** If text delivery works but media fails, patch media transfer helpers rather than generic gateway routing.
4. **Preserve gateway invariants.** Do not break prompt caching, message role alternation, access-policy checks, token locks, or profile-safe paths.
5. **Use focused regression tests.** Add tests around the helper or adapter seam that reproduces the exact failure mode.

## Workflow

1. **Read logs first**
   - `~/.hermes/logs/gateway.log` for adapter lifecycle and delivery errors.
   - `~/.hermes/logs/errors.log` for stack traces and repeated warnings.
   - Look for platform names (`weixin`, `telegram`, `feishu`, etc.), `response ready`, `Sending response`, `send failed`, and adapter-specific errors.
2. **Trace the path**
   - Platform config: `gateway/config.py`.
   - Adapter: `gateway/platforms/<platform>.py` or plugin platform adapter.
   - Cross-platform sending: `tools/send_message_tool.py`.
   - Session routing: `gateway/session.py`, `gateway/run.py` when needed.
3. **Build a tight loop**
   - Prefer an existing focused test file such as `tests/gateway/test_<platform>.py`.
   - If reproducing a network failure, use stub sessions/mocked requests to model the failing boundary deterministically.
4. **Patch narrowly**
   - Keep changes local to the failing adapter/helper unless the same bug class exists across siblings.
   - For transient network failures, prefer bounded retries with clear logging over broad sleeps or unbounded loops.
   - Re-raise `asyncio.CancelledError` immediately in retry wrappers.
5. **Verify and restart when applicable**
   - Run focused tests with `scripts/run_tests.sh`.
   - If the live gateway should pick up code changes, restart it and confirm status/logs show the affected platform connected.

## Weixin media transfer pitfall

For Weixin/iLink media failures, see `references/weixin-media-transfer-retries.md`.

The short version: if text messages work but images/files fail with transient `Cannot connect to host novac2c.cdn.weixin.qq.com` errors, add bounded retries around the media transfer helpers (`_download_bytes`, `_upload_ciphertext`) while preserving `asyncio.wait_for()` and avoiding aiohttp `timeout=` kwargs.

## Proxy and TUN diagnostic

For macOS Discord + Clash/Mihomo TUN/proxy layering, see `references/discord-tun-proxy.md`.
When a platform receives inbound events and the agent reaches `response ready` but outbound send fails with TLS resets/timeouts, inspect proxy layering before changing the adapter. On macOS, `resolve_proxy_url` may auto-detect `scutil --proxy` even when Clash/Mihomo is already running in global TUN mode. This can create a duplicate path: adapter HTTP proxy → TUN proxy. Check `lsof -nP -iTCP:<port> -sTCP:LISTEN`, `scutil --proxy`, the active Clash `tun.enable/auto-route` configuration, and logs for `Using proxy for Discord` or equivalent.

For a TUN/global setup, prefer one path: keep TUN/global routing and disable the macOS HTTP/HTTPS/SOCKS system proxy, then restart the affected profile. Do not infer that gateway state `connected` means outbound delivery works; verify a real send or inspect `response ready` followed by `send failed`.

## Verification commands

```bash
scripts/run_tests.sh tests/gateway/test_<platform>.py -q
hermes gateway status
hermes gateway restart
```

Use the installed venv launcher (`venv/bin/hermes ...`) if the repository checkout's shell PATH does not resolve the same Hermes binary.
