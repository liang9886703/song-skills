# Cloudflare Tunnel + Clash/Mihomo: Error 1033

## Symptom

The visitor gets Cloudflare Error 1033 while the local service (for example `127.0.0.1:8080`) is healthy. This means the Cloudflare edge cannot see a registered `cloudflared` connector; it is not evidence that the visitor-facing hostname rule is wrong.

## Reproduction/diagnosis

1. Inspect the actual `cloudflared` process and its launchd plist. Verify the token path and whether the owning service is the system daemon or the user LaunchAgent.
2. Read the cloudflared stderr log. The useful sequence is:
   - region endpoint DNS resolution
   - TCP/UDP 7844 connectivity
   - `Registered tunnel connection`
   - origin request errors, if any
3. Inspect Clash/Mihomo runtime state through the Unix controller, not just YAML:
   - `GET /configs`
   - `GET /rules`
   - `GET /connections` while restarting or probing the tunnel
4. In fake-IP mode, if `region*.v2.argotunnel.com` resolves to `198.18.x.x`, add this to `dns.fake-ip-filter`:

```yaml
- +.argotunnel.com
```

5. If the real endpoint is reachable only through the proxy, use rules before broad GeoSite/GeoIP/MATCH rules:

```yaml
- DOMAIN-SUFFIX,argotunnel.com,IpEqual
- DST-PORT,7844,IpEqual
```

Keep the tunnel process on HTTP/2 when QUIC is blocked:

```xml
<string>--protocol</string>
<string>http2</string>
```

6. Reload the active Mihomo config through its supported API, then restart only the owning cloudflared service. On macOS, a user LaunchAgent can be loaded/restarted with `launchctl bootstrap gui/<uid> <plist>` and `launchctl kickstart -k gui/<uid>/<label>`; a system LaunchDaemon needs administrator privileges.

## Verification

Do not declare recovery from a browser `302` or Access login `200`. Require all of:

- cloudflared log: `DNS Resolution ... PASS`
- cloudflared log: `TCP Connectivity ... PASS` (or a successful QUIC check)
- cloudflared log: `Registered tunnel connection ... protocol=http2` or `protocol=quic`
- local upstream still returns the expected HTTP status
- public hostname no longer returns Error 1033

If the host resolver cannot resolve the region names but DoH through the proxy can, use a resolver path visible to the cloudflared process. As a temporary, monitored workaround, verified current region A records can be placed in `/etc/hosts`; treat them as expiring operational data and refresh them rather than hard-coding them permanently.
