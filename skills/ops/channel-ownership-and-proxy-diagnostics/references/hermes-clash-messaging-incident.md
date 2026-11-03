# Hermes + Clash messaging incident reference

## Reproduction pattern

1. Hermes owns Discord in one or more profiles; OpenClaw may still contain stale/copied Discord accounts.
2. Clash/Mihomo uses TUN with fake-IP DNS and a China-direct policy.
3. A shared outage produces Discord `ClientConnectorDNSError` / `socket_closed` and Weixin `poll error` for `ilinkai.weixin.qq.com` in the same time window.
4. Some curl/browser requests may still work through TUN while Hermes' explicit aiohttp proxy path fails.

## Verification recipe

```bash
scutil --proxy
lsof -nP -iTCP:7897 -sTCP:LISTEN
ps -ww -axo pid,command | grep -Ei 'clash|mihomo|sing-box'
```

Query `/configs`, `/rules`, `/proxies`, and `/connections` over `/tmp/verge/verge-mihomo.sock`. Check that TUN/fake-IP is enabled, the mixed port is usable, and the selected chain is alive.

For China-direct Weixin, keep rules such as:

```yaml
- DOMAIN-SUFFIX,weixin.qq.com,DIRECT
- DOMAIN-SUFFIX,wechat.com,DIRECT
```

and add to `dns.fake-ip-filter`:

```yaml
- +.weixin.qq.com
- +.wechat.com
```

Keep foreign-service rules such as Discord above `GEOSITE,CN,DIRECT` and `GEOIP,CN,DIRECT`. After editing the Clash Verge enhancement/override, back up generated YAML, reload with Mihomo `PUT /configs` and require `204`, flush DNS, then verify Weixin resolves to real IPs while Discord remains routed through the proxy group.
