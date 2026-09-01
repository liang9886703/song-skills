---
name: vpn-proxy-diagnostics
description: Use when a VPN/proxy cannot reach a domain.
---

# VPN / Proxy Diagnostics

Use this skill when a site is unreachable through Clash/Mihomo, sing-box, or a similar rule-based VPN, including cases where a public domain terminates at Cloudflare and tunnels to a local service.

## Operating principles

1. Diagnose the active runtime, not only a profile file. Identify the client process, effective config path, TUN interface, DNS mode, proxy listener, and local upstream service.
2. Separate the layers:
   - DNS resolution and whether the answer is a fake-IP address.
   - Rule classification and rule ordering.
   - Selected proxy group / actual outbound node.
   - Cloudflare edge or Access redirect domains.
   - Tunnel-to-local-service health.
3. Prefer the smallest explicit rule change. Add a host-specific rule before broad GeoSite/GeoIP/MATCH rules when classification is ambiguous; do not casually change tunnel transport rules or force a public tunnel domain DIRECT. Treat `GEOIP,CN,DIRECT` as an IP-location fallback, never as proof that the service is Chinese: CDN/shared/DNS-contaminated addresses can be geographically CN while the hostname needs proxying. For messaging services such as Weixin, use explicit domain-level `DIRECT` rules for `weixin.qq.com`/`wechat.com` before broad rules.
4. Before editing a generated or user-managed config, make a timestamped backup. Never expose credentials, UUIDs, tokens, or full proxy definitions in the final response.
5. Apply changes through the client’s supported reload API or UI when available. Do not assume that editing a generated file automatically changes the running runtime.
6. Verify the whole chain after the change: local listener, DNS/fake-IP route, rule table, proxy request, Cloudflare response/redirect, and (where possible) the application response.

## Clash Verge / Mihomo workflow on macOS

1. Discover the runtime:
   - `ps aux | egrep -i 'clash|mihomo|sing-box|surge|v2ray|xray|vpn'`
   - `scutil --proxy`
   - `lsof -nP -iTCP:<port> -sTCP:LISTEN`
2. Inspect the active config path from the process command line. On Clash Verge Rev it is commonly under `~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/`.
3. Read only the relevant sections: `dns.enhanced-mode`, `fake-ip-range`, `tun`, `proxy-groups`, and `rules`. Do not print the whole config if it contains credentials.
4. Query the Mihomo Unix controller when configured, commonly `/tmp/verge/verge-mihomo.sock`:
   - `GET /configs` confirms TUN and mode.
   - `GET /rules` confirms the effective, loaded rule order.
   - `GET /proxies` confirms the selected group/node.
   - `GET /connections` can show host, remote destination, chain, rule, and rule payload while a request is active.
5. For a fake-IP setup, expect a public hostname to resolve to the configured fake range (often `198.18.0.0/16`) and route through the TUN interface. Do not mistake that synthetic address for the real Cloudflare edge IP.
6. Back up the config, then insert explicit rules before broad rules. For a Cloudflare-protected app, usually cover the app hostname and the Cloudflare Access redirect suffix (for example `cloudflareaccess.com`) with the intended proxy group. Add other Cloudflare suffixes only when observed in the redirect/connection trace; avoid broad speculative rules.
7. Hot-reload using Mihomo’s supported config endpoint, e.g. `PUT /configs` with `{"path":"<active-config>","force":true}` over the Unix socket. Confirm `204`, then query `/rules` again to prove the runtime accepted the change.
8. Flush local DNS cache if the client or browser retains stale resolution, then retry with the browser. On macOS, `dscacheutil -flushcache` is sufficient in many cases; `killall -HUP mDNSResponder` may require elevated privileges and can be skipped if unavailable.

## Verification matrix

- Local service: `curl -sS -D- http://127.0.0.1:<upstream>/` and confirm an expected HTTP status.
- DNS: inspect the hostname and confirm whether fake-IP is expected.
- Rule load: query `/rules`; the explicit host rule must appear before GeoSite/GeoIP/MATCH.
- External path: use `curl -x http://127.0.0.1:<mixed-port> -L -D- https://<host>/` and inspect status, `Location`, `server`, and Cloudflare ray headers.
- Cloudflare Access: a `302` to the Access login followed by `200` for the login page proves the edge and Access redirect path work; it does not prove authentication or the protected app content.
- Tunnel: a healthy local 8080 response proves only the local upstream is listening; correlate with cloudflared logs or an authenticated end-to-end response when tunnel behavior itself is in doubt.

## Cloudflare Tunnel 1033 recovery

When the visitor receives Error 1033, the public edge is reachable but no healthy connector is registered. Diagnose the tunnel side separately from the visitor request:

1. Read cloudflared stderr and look for `region*.v2.argotunnel.com`, port 7844 failures, `there are no free edge addresses left to resolve to`, and `Registered tunnel connection`.
2. In fake-IP mode, add `+.argotunnel.com` to `dns.fake-ip-filter`; a DIRECT rule alone does not undo a synthetic DNS answer.
3. If the host resolver cannot resolve the region endpoints but DoH through the proxy can, use a resolver path that works for the owning process or short-lived, verified hosts entries for the current region addresses. Restart the owning launchd service after changing DNS inputs.
4. If connectivity checks show TCP 7844 blocked, route `DOMAIN-SUFFIX,argotunnel.com` and `DST-PORT,7844` through the selected proxy group. Use `--protocol http2` when QUIC is blocked.
5. Do not stop at a Cloudflare `302`/Access `200`: that proves only the edge/Access path. Require fresh `Registered tunnel connection ... protocol=http2` log lines and then retest the public hostname.

See `references/cloudflare-tunnel-clash.md` for the focused diagnostic sequence and rule ordering.


- A `MATCH` rule may already proxy a domain; lack of an explicit Cloudflare rule is not by itself proof of the failure. Use effective `/rules`, active connections, and a controlled request before changing policy.
- Do not assume the cloudflared tunnel’s own transport should be DIRECT. In a fake-IP TUN setup, `DOMAIN-SUFFIX,argotunnel.com,DIRECT` can still resolve to synthetic `198.18.x.x` addresses, and direct TCP/UDP 7844 may be blocked. Use cloudflared logs and active connections to decide; if direct 7844 fails, exclude the tunnel endpoint from fake-IP and route `argotunnel.com` plus port `7844` through the working proxy group. Keep `--protocol http2` when QUIC is unavailable.
- A successful `curl` with an HTTP proxy can hide a browser/TUN difference. Test both the actual TUN path and the explicit mixed-port path when possible.
- Rule changes to a generated config can be overwritten by Clash Verge profile updates. After a successful fix, identify whether the change belongs in the profile override/template rather than only the generated YAML.
- Never report “fixed” solely because DNS resolves. Require runtime rule confirmation and an HTTP response.

## Reference

See `references/cloudflare-fake-ip-local-tunnel.md` for a compact reproduction and verification recipe for Cloudflare Access plus a local 8080 upstream.
