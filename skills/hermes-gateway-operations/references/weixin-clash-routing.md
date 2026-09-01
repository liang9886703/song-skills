# Weixin + Clash/Mihomo routing notes

Use this reference when Weixin ingress works but Hermes cannot poll or send through a macOS Clash Verge TUN.

## Diagnostic pattern

- Gateway log sequence to distinguish layers:
  - `[Weixin] inbound` = message reached the adapter.
  - `response ready` = agent turn completed.
  - `Sending response` followed by `send failed` = outbound transport failure.
- `gateway_state.json: connected` only describes adapter startup; it is not proof of a successful poll/send cycle.
- A fake-IP result such as `198.18.x.x` indicates Clash fake-IP DNS mapping. It is not the Tencent service address.

## Safer Clash fix

Prefer, in this order:

1. Exclude the service from fake-IP DNS: `+.weixin.qq.com` and the relevant CDN suffix (for example `+.cdn.weixin.qq.com`).
2. Add `DOMAIN-SUFFIX,weixin.qq.com,DIRECT` and the CDN domain rule before broad `GEOSITE,CN`/`GEOIP,CN` rules.
3. If required, add narrow `IP-CIDR,...,DIRECT,no-resolve` rules for currently observed endpoint /24s. Treat these as volatile adjuncts, not authoritative permanent Tencent ranges.

Do not use a broad `43.0.0.0/8`, `180.0.0.0/8`, or all-Tencent allowlist just to fix one endpoint. Re-query DNS after changes; CDN and iLink addresses can rotate.

## Operational cautions

- Clash Verge may regenerate or overwrite its generated YAML on profile reload. Re-read both the file and the live Unix API after applying changes.
- Preserve the user's current `mode` (Rule vs Global); reloading a stale generated file can silently change it.
- Verify with the same client stack as the adapter. A system `curl` returning `405 Method Not Allowed` proves TLS/HTTP reachability for curl, not that Python `aiohttp` can send successfully.
- Finish with a real inbound/outbound message test; do not declare success from a connected state alone.
