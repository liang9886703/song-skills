---
name: codex-desktop-network-debugging
description: "Use when Codex WebSockets fail behind Clash."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [codex, desktop, websocket, clash, mihomo, vpn, fake-ip, tun, openai]
    related_skills: [messaging-network-diagnostics, vpn-proxy-diagnostics]
---

# Codex Desktop Network Debugging

Use this class-level workflow when the ChatGPT/Codex desktop app reports connection loss, streaming interruption, repeated reconnects, or WebSocket failures while a rule-based VPN is active.

## Diagnostic model

Separate the problem into four paths:

1. **Codex application path** — confirm the desktop app and its `codex app-server` are alive; inspect open sockets and app diagnostics without exposing credentials.
2. **Clash runtime path** — query the active Mihomo controller for mode, effective rules, selected proxy group/node, and active connections. A generated YAML file can disagree with runtime mode after a GUI mode toggle.
3. **Name/routing path** — distinguish fake-IP DNS from real destination IPs and inspect the actual matched rule. Do not infer from the rule file alone.
4. **Transport path** — correlate the first failed connection with the application symptom. A WebSocket close/reconnect is downstream evidence; a `DIRECT` dial timeout or reset is the actionable failure.

## Core workflow

1. Identify the active Clash/Mihomo process, active config path, Unix controller socket, mixed port, and TUN interface.
2. Record the current mode before changing anything. Preserve the user's intended mode; Global is a useful control experiment, not a durable fix.
3. Query effective `/configs`, `/rules`, `/proxies`, and `/connections` through the active controller. Prefer runtime evidence over stale generated files.
4. Filter Clash logs around the failure for the provider's domains and transport errors. Look specifically for lines such as:
   - `match ... using IpEqual[...]` — expected proxied path;
   - `dial DIRECT (match GeoIP/cn) ... timeout` — likely rule bypass;
   - `using GLOBAL` — control path after a mode switch, not proof that Rule mode is healthy.
5. Enumerate the actual provider hostname family from connections/logs. For Codex/ChatGPT this commonly includes `chatgpt.com`, `ws.chatgpt.com`, `ab.chatgpt.com`, `chat.openai.com`, `api.openai.com`, `auth.openai.com`, and `files.openai.com`; verify against the current trace rather than assuming a fixed list.
6. If a provider hostname can be classified by `GEOSITE,CN` or `GEOIP,CN`, add explicit provider-domain rules **before** those broad direct rules. Fake-IP/TUN makes this failure mode possible even for an overseas service.
7. Put the durable rule in the Clash GUI's active profile enhancement/override layer, not only in the generated merged YAML. Back up both files before manual edits when a runtime emergency requires updating the active file immediately.
8. Hot-reload through the supported Mihomo controller endpoint when available. Confirm the response, then verify `/configs` is back in Rule mode and `/rules` shows the explicit rules at the top.
9. Require fresh evidence after reload: a new Codex connection, a log line showing the explicit domain rule and proxy chain, and no new direct timeout for the provider. Existing connections from Global mode are not sufficient.

## Rule design

- Prefer narrow `DOMAIN-SUFFIX` rules to broad provider IP ranges.
- Put service rules ahead of `GEOSITE,CN` and `GEOIP,CN`; otherwise a CN-classified destination can bypass the proxy.
- Use the provider's parent suffix to cover WebSocket and auxiliary subdomains. For example, `DOMAIN-SUFFIX,chatgpt.com,IpEqual` covers `ws.chatgpt.com` and `ab.chatgpt.com`; pair it with `DOMAIN-SUFFIX,openai.com,IpEqual` for the separate API/auth/file hosts.
- Do not add speculative `DIRECT` rules for Cloudflare, tunnel, or provider domains. Confirm the actual connection and rule first.
- Keep the selected proxy group/node unchanged while testing routing so that rule correctness is not confounded with node quality.

## Verification checklist

- Controller reports `mode: rule`.
- Effective rule list has the explicit provider rules before CN rules.
- Active Codex connections show fake-IP inbound but the intended proxied chain.
- Fresh log lines show `DomainSuffix(...) using <intended group/node>` rather than `DIRECT`.
- No fresh `dial DIRECT ... timeout` / reset for the provider.
- Codex app-server remains alive and its process retains the expected proxy/TUN sockets.

See `references/codex-clash-reproduction.md` for the concrete incident pattern and controller commands.
