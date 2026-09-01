# Cloudflare + fake-IP + local tunnel reference

## Symptom pattern

- A browser cannot reach a Cloudflare-protected hostname.
- The hostname resolves to a synthetic `198.18.x.x` address because Mihomo uses fake-IP DNS.
- A local application is healthy on `127.0.0.1:8080`.
- The public hostname redirects to a `*.cloudflareaccess.com` login host.

## Minimal probe sequence

```sh
# Identify the active TUN/proxy runtime and local upstream
ps aux | egrep -i 'clash|mihomo|sing-box|surge|v2ray|xray|vpn'
lsof -nP -iTCP:8080 -sTCP:LISTEN
dig +short app.example.com
route -n get 198.18.0.1

# Use the active Mihomo Unix controller, if present
# GET /configs, /rules, /proxies, /connections

# Check the upstream and browser-facing path separately
curl -sS -D- http://127.0.0.1:8080/ -o /tmp/upstream.body
curl -x http://127.0.0.1:7897 -L -D /tmp/headers -o /tmp/page.html \
  --connect-timeout 8 --max-time 20 https://app.example.com/
```

## Interpretation

- `198.18.0.0/16` is a fake-IP range, not the origin or Cloudflare edge.
- An explicit `DOMAIN,app.example.com,<proxy-group>` rule should precede broad GeoSite/GeoIP/MATCH rules when classification is uncertain.
- If the response is a `302` to `*.cloudflareaccess.com` and the follow-up returns `200`, Cloudflare edge plus Access login routing is working. Authentication is a separate concern.
- A local `200` from port 8080 proves the upstream is listening, not that the cloudflared tunnel is healthy.

## Safe reload pattern

1. Copy the active YAML to a timestamped `.bak` file.
2. Patch only the required domain rules.
3. Reload through Mihomo’s controller, for example `PUT /configs` with the active config path and `force: true`.
4. Query `/rules` and verify the new rules are loaded before claiming success.

Avoid printing the full YAML: proxy credentials, UUIDs, tokens, and private endpoints may be embedded in it.
