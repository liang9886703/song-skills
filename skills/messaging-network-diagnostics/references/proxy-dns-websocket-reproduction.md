# Proxy/DNS/WebSocket reproduction notes

## Clash + Weixin

- A configured/connected Weixin adapter can still fail both polling and sending at the TLS layer.
- Distinguish system `curl` from Python `aiohttp`/`httpx`: SecureTransport-backed curl may succeed while Python OpenSSL reports `SSL record layer failure`.
- Clash fake-IP addresses such as `198.18.0.0/16` are not provider subnets. For clients that resolve locally, add the provider domains to `dns.fake-ip-filter`; then verify the resolver returns real addresses.
- Prefer `DOMAIN-SUFFIX,weixin.qq.com,DIRECT` plus fake-IP exclusion. Current provider IPs are dynamic; narrow CIDRs are only a supplementary, temporary measure.

## OpenClaw + Discord

- Hermes status can report Discord unconfigured while OpenClaw owns multiple active Discord accounts.
- Inspect `~/.openclaw/logs/gateway.log`; the useful sequence is provider startup, `gateway proxy enabled` (if configured), client initialization, and whether WebSocket readiness follows.
- `Gateway websocket closed: 1006` is a transport failure. It does not by itself prove token invalidity.
- OpenClaw supports per-account `channels.discord.accounts.<id>.proxy`. Validate with `openclaw config set --batch-json ... --dry-run`, then apply and restart the OpenClaw launchd service.
- A Discord REST request can work while WebSocket fails. Test both the API endpoint and the gateway WebSocket path.
- Be careful with Clash rules: if the OpenClaw client explicitly uses the local HTTP proxy, a `DIRECT` rule for Discord can override the intended proxy path. Route through the selected proxy when the direct WebSocket path closes.
- `getaddrinfo ENOTFOUND discord.com` can persist despite curl resolving the name; compare Node's resolver path with Clash's DNS and the proxy agent separately.

## Safety

- Never print Discord bot tokens or Weixin credentials while inspecting account maps.
- Verify runtime state after reloads because Clash Verge may regenerate its YAML and OpenClaw may hot-reload config.
- Do not claim recovery from `configured` or `client initialized` alone; require a fresh ready/connected event or successful inbound/outbound message.
