---
name: channel-ownership-and-proxy-diagnostics
description: "Use when channels fail across runtimes or proxy/TUN paths."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [messaging, hermes, openclaw, discord, weixin, proxy, tun, fake-ip, dns]
    related_skills: [hermes-gateway-debugging, messaging-network-diagnostics, vpn-proxy-diagnostics]
---

# Channel Ownership and Proxy Diagnostics

Use this class-level workflow when Discord, Weixin/WeChat, or several messaging channels fail and Hermes/OpenClaw ownership or Clash/Mihomo routing is ambiguous.

## 1. Establish the owner before acting

- Do not infer ownership from whichever runtime reports a configured channel.
- Inspect both runtimes, then inspect actual adapter logs and process arguments.
- Hermes-owned Discord evidence includes profile config entries and log namespaces such as `hermes_plugins.discord_platform.adapter`, `inbound message`, `response ready`, and `Sending response`.
- Do not start or restart OpenClaw merely because it has a copied/stale Discord configuration. Restart only the owning gateway.
- Keep channel credentials and account routing unchanged during network diagnosis.

## 2. Correlate failures across channels

Separate configuration, DNS, routing, transport, and application layers. Correlate timestamps across the owning gateway logs.

- Discord `ClientConnectorDNSError`, TLS reset, WebSocket `socket_closed`, and reconnect loops are transport symptoms.
- Weixin `poll error` to `ilinkai.weixin.qq.com` at the same time as Discord failures is strong evidence of a shared network path problem.
- A later `Connected`/`reconnected successfully` proves recovery at that moment, not sustained health; verify fresh traffic.
- Do not blame model/API failures on the channel when logs show `response ready` followed by a send.

## 3. Diagnose Clash/Mihomo layering

On macOS inspect:

```bash
scutil --proxy
lsof -nP -iTCP:<mixed-port> -sTCP:LISTEN
ps -ww -axo pid,command | grep -Ei 'clash|mihomo|sing-box'
```

Query the active Unix controller when present:

```text
/tmp/verge/verge-mihomo.sock
```

Use `/configs`, `/rules`, `/proxies`, and `/connections` to verify runtime state rather than trusting generated YAML. Check whether TUN/fake-IP is enabled, whether the mixed-port is usable, and which proxy chain/rule is selected.

A system proxy pointing to `127.0.0.1:7897` while the listener is absent or unstable is a concrete failure. TUN may still make curl/browser requests work, so compare the actual client path used by Hermes with explicit-proxy and TUN/direct probes.

## 4. Apply China-direct policy safely

For the intended policy—China services direct, foreign services proxied—use this ordering:

1. Explicit foreign-service domain rules (`discord.com`, `gateway.discord.gg`, OpenAI/ChatGPT, etc.) to the proxy group.
2. Explicit domestic-service domain rules (`weixin.qq.com`, `wechat.com`) to `DIRECT`.
3. `GEOSITE,CN,DIRECT` and `GEOIP,CN,DIRECT` as broad fallbacks.
4. `MATCH,<proxy-group>` as the final fallback.

Never let `GEOIP,CN` override domain intent for CDN/shared IPs.

With fake-IP DNS, a direct rule alone is insufficient. Add direct service domains to `dns.fake-ip-filter`, for example:

```yaml
- +.weixin.qq.com
- +.wechat.com
```

Then the domestic service resolves to its real IP before `DIRECT`, instead of trying to connect directly to a synthetic `198.18.x.x` address.

## 5. Edit and verify persistently

- Back up generated Clash YAML before any live edit.
- Prefer the Clash Verge profile enhancement/override as the durable source; generated YAML may be rewritten on profile reload.
- If a live reload is needed, use the Mihomo controller's supported `PUT /configs` reload and require HTTP `204`.
- Verify the generated file contains fake-IP exclusions, `/rules` retains foreign-proxy and domestic-direct ordering, DNS returns real IPs for excluded domestic domains, and owning Hermes logs show fresh reconnect/traffic.
- Do not report success from a stale `connected` status alone.

## Pitfalls

- `hermes status --all` on the default profile can say Discord is unconfigured while another Hermes profile owns it.
- OpenClaw status can show active Discord accounts without owning the channel in the current setup.
- A successful curl through TUN does not prove Hermes' explicit aiohttp/HTTP proxy path works.
- A direct Chinese IP classification is not proof that the hostname should be direct; use explicit domain rules for services with CDN/shared addresses.
- If a patch to generated YAML changes an unrelated line, restore that line before reloading and verify the diff.

## Reference

See `references/hermes-clash-messaging-incident.md` for a condensed reproduction and verification recipe.
