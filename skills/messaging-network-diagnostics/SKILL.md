---
name: messaging-network-diagnostics
description: Use when messaging channels fail.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [messaging, gateway, discord, weixin, wechat, proxy, dns, tls, websocket, troubleshooting]
---

# Messaging Network Diagnostics

Use this class-level skill when Telegram, Discord, Weixin/WeChat, Feishu, or another gateway channel is configured but appears disconnected, receives messages without replying, or repeatedly reconnects.

## Core workflow

1. Identify the actual runtime.
   - Check whether the channel belongs to Hermes Gateway, OpenClaw, or another process.
   - Do not infer from Hermes' default profile status when OpenClaw owns the channel.
   - Inspect the supervising service, process, and channel-specific logs.

2. Separate the path into layers.
   - Configuration: credentials/account enabled and channel policy.
   - DNS: system resolver result, fake-IP result, and authoritative/DoH result.
   - Routing: Clash mode, rule match, selected proxy chain, and TUN/fake-IP behavior.
   - Transport: HTTP API, TLS handshake, WebSocket gateway, and adapter retries.
   - Application: inbound event, agent response generation, outbound send.

3. Prove inbound and outbound independently.
   - A channel can be `connected` while polling or sending is failing.
   - For "no reply", look for `inbound message`, `response ready`, and `send failed` in order.
   - Report the first failed layer; do not call a configured or initialized adapter healthy without recent traffic evidence.

4. Compare clients and paths.
   - Test the target endpoint with both direct and explicit local HTTP proxy paths.
   - A successful system `curl` does not prove Python/Node TLS or WebSocket compatibility.
   - If HTTP works but WebSocket fails, inspect gateway-specific proxy support and DNS resolution separately.

5. Configure the owning client explicitly.
   - For OpenClaw Discord, use per-account `channels.discord.accounts.<id>.proxy`, not only macOS system proxy settings.
   - Validate with `openclaw config set ... --dry-run` before writing; restart the owning gateway after applying.
   - Never print or copy bot tokens while inspecting multi-account configuration.

6. Handle Clash carefully.
   - Preserve the user's selected mode; do not silently replace Global with Rule or vice versa during a config reload.
   - Prefer domain rules and fake-IP exclusions for dynamic services over broad IP ranges.
   - If a client explicitly uses the Clash HTTP proxy, do not add a conflicting `DIRECT` rule for the same domain unless testing proves it is required.
   - For rule-mode diagnosis, inspect the actual matched rule and chain through the Clash API, not just the YAML file.
   - Generated Clash files may be rewritten by the GUI; verify runtime state after reload.

7. Verify recovery.
   - Re-read runtime mode and matched rules.
   - Restart only the owning gateway when possible.
   - Require fresh logs showing adapter readiness or successful inbound/outbound traffic; old `connected` state is insufficient.

## Pitfalls

- Hermes `status --all` may say Discord is not configured while OpenClaw has active Discord accounts. Check both runtimes before changing credentials.
- A WebSocket close code `1006` is a transport symptom, not proof of an invalid Discord token.
- OpenClaw may log `getaddrinfo ENOTFOUND` even when `curl` resolves the same domain through Clash; Node's resolver and the HTTP proxy path must be tested separately.
- A local proxy can be active for REST requests while gateway WebSockets still fail. Confirm explicit gateway-proxy support in logs.
- Do not broaden a Tencent/Discord allowlist to entire provider ASNs as a first fix. Prefer exact domains, current narrow CIDRs only when necessary, and note that provider IPs are dynamic.
- If a change to a generated config is overwritten, use the owning application's supported config mechanism or reapply through its active profile; do not assume the file is durable.

## References

- `references/proxy-dns-websocket-reproduction.md` — condensed reproduction and verification patterns for Clash + Hermes/OpenClaw channel failures.
