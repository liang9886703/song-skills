# Discord + macOS TUN/proxy diagnosis

## Failure signature

- Profile state says `connected`.
- Inbound Discord messages are logged.
- Agent logs `response ready`.
- Outbound logs show `Cannot connect to host discord.com:443`, `ConnectionResetError`, or aiohttp `_create_proxy_connection` / `_start_tls_connection`.
- Adapter startup says `Using proxy for Discord: http://127.0.0.1:<port>`.

## Checks

```bash
scutil --proxy
lsof -nP -iTCP:<port> -sTCP:LISTEN
ps axww | grep -Ei 'Clash Verge|verge-mihomo|mihomo|sing-box'
grep -nE '^(mixed-port|socks-port|tun:|  enable:|  auto-route:)' "$HOME/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml"
```

Inspect the Discord adapter's proxy resolution path: `DISCORD_PROXY` takes priority, then generic proxy environment variables, then macOS `scutil --proxy`. A TUN config with `tun.enable: true` and `auto-route: true` already routes traffic globally; adding the macOS HTTP/HTTPS/SOCKS proxy can create a duplicate proxy path.

## Preferred recovery

Keep Clash/Mihomo TUN/global routing and disable the macOS HTTP/HTTPS/SOCKS system proxy. Restart the affected gateway profile from an external shell, then verify new logs no longer say `Using proxy for Discord` and confirm a real outbound message. Do not treat a cached `gateway_state.json` value of `connected` as delivery proof.
