---
name: hermes-gateway-operations
description: Use when operating Hermes messaging gateways.
---

# Hermes Gateway Operations

Use this for practical operation of Hermes messaging gateways: checking platform health, reading gateway state/logs, restarting after updates, and explaining channel availability.

## Channel health workflow

1. **Check gateway state before guessing.** Inspect `$HERMES_HOME/gateway_state.json` or `hermes status --all` for platform states.
2. **Use logs to distinguish configured vs usable.** A platform can be configured but still failing startup/retry. Prefer recent gateway logs over config presence.
3. **Report states separately.** Use categories like `connected`, `retrying`, `configured but failing`, and `not configured`.
4. **Look for heartbeat/polling evidence.** If the user says “if it works there will be heartbeats,” inspect logs/state for inbound events, polling restarts, gateway heartbeats, and platform-specific startup errors.

## Restarting after an update

A gateway process usually cannot restart/stop itself safely from inside the live gateway conversation. If `hermes gateway restart` is blocked because it is being called from inside the gateway process, use an external supervisor or delayed launchd job.

macOS launchd deferred restart pattern:

```bash
mkdir -p "$HOME/.hermes/logs"
launchctl remove ai.hermes.deferred-gateway-restart 2>/dev/null || true
launchctl submit -l ai.hermes.deferred-gateway-restart -- /bin/bash -lc 'sleep 3; hermes gateway restart >> "$HOME/.hermes/logs/restart-after-update.log" 2>&1'
```

Then verify:

```bash
sleep 5
hermes gateway status
hermes --version
tail -80 "$HOME/.hermes/logs/restart-after-update.log"
```

## Channel-specific network troubleshooting

For Weixin/WeChat or other channels behind a local proxy/TUN. See `references/weixin-clash-routing.md` for the reusable Clash/Mihomo recipe:

1. Separate ingress from egress. Confirm an inbound event, agent response generation, and outbound send independently in the gateway log. A `connected` platform state only proves adapter startup; it does not prove polling or sending works.
2. With Clash/Mihomo fake-IP DNS, inspect the live runtime mode and DNS mapping before editing anything. A hostname resolving to `198.18.0.0/16` is a fake-IP path, not the remote service's real address.
3. Prefer a domain-level `DIRECT` rule plus fake-IP exclusion for the service domain (for Weixin, `+.weixin.qq.com` and relevant CDN subdomains). Use narrow `IP-CIDR` rules only as an adjunct for currently observed addresses; Tencent/CDN addresses are dynamic and shared, so never generalize to a broad Tencent allocation without justification.
4. Do not assume a successful `curl` probe proves Python/aiohttp can send. Test with the same client stack used by the adapter, and verify a real outbound message after configuration changes.
5. Clash Verge generated YAML can be overwritten by the GUI/profile reload. Re-read the file and the Clash Unix API after every reload; preserve the user's existing mode (Rule/Global) instead of inferring it from a stale generated file. Validate YAML structure before applying it.
6. When a config reload changes routing mode unexpectedly, restore the user's chosen mode first, then verify the target domain rule. Do not silently leave Global/Rule changed.

## Pitfalls

- Do not equate “configured” with “usable.” Confirm runtime state/logs.
- For messaging channels, do not stop at `response ready`; require `send succeeded` or an actual user-visible reply. `response ready` followed by TLS/send errors means the channel is ingress-healthy but egress-broken.
- If Telegram shows polling conflicts, mention that another process may be using the same bot token, while the gateway may still report connected.
- If Feishu/other SDK startup fails after a Hermes update, report the exact compatibility error but avoid hard-coding it as a permanent tool limitation.
- Do not expose tokens, bot secrets, app secrets, cookies, connection strings, or auth JSON contents in summaries.
