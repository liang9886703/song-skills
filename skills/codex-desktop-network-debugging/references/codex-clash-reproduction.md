# Codex + Clash rule-bypass reproduction

## Incident signature

A Codex desktop session repeatedly loses streaming/WebSocket connections in Clash Rule mode, while switching Clash to Global immediately restores traffic.

The decisive log pattern is not a generic WebSocket close. It is a provider connection bypassing the proxy:

```text
dial DIRECT (match GeoIP/cn) ... --> chatgpt.com:443 error: dial tcp <resolved-ip>:443: i/o timeout
```

The same session may show successful connections using the intended proxy group before the failure, which means the node itself is not sufficient evidence of the root cause.

## Effective runtime checks

For Clash Verge Rev with the usual Mihomo Unix controller:

```bash
curl --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/configs
curl --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/rules
curl --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/proxies
curl --unix-socket /tmp/verge/verge-mihomo.sock http://localhost/connections
```

Check all of the following:

- `/configs` reports the actual mode; do not trust a stale `mode: rule` in a generated file after a GUI toggle.
- `/rules` places explicit provider rules ahead of `GEOSITE,CN` and `GEOIP,CN`.
- `/connections` shows fake-IP inbound as expected, but the intended proxy chain for provider hosts.
- `/proxies` confirms the selected group and node are alive.

## Minimal durable fix pattern

Add provider suffix rules to the active profile's enhancement/override file:

```yaml
prepend:
- DOMAIN-SUFFIX,chatgpt.com,IpEqual
- DOMAIN-SUFFIX,openai.com,IpEqual
```

For an emergency reload, update the generated merged config too, then reload the active file through Mihomo:

```bash
curl --unix-socket /tmp/verge/verge-mihomo.sock \
  -X PUT http://localhost/configs \
  -H 'Content-Type: application/json' \
  --data '{"path":"<active-config>","force":true}'
```

A successful reload returns HTTP 204. Re-query `/configs` and `/rules`; do not call the fix complete based on the HTTP status alone.

## Verification evidence

Fresh log lines should look like:

```text
chatgpt.com:443 match DomainSuffix(chatgpt.com) using IpEqual[<node>]
```

The Codex process should remain alive and retain active connections to Clash/TUN. Existing connections created while Global was active do not prove Rule mode recovery; wait for or trigger a fresh provider connection.

## Durability and safety

- Back up the active profile enhancement file and generated merged config before manual edits.
- Prefer the enhancement/override layer because subscription refreshes can regenerate the merged file.
- Do not print subscription URLs, UUIDs, API keys, or full proxy definitions in reports.
- Keep the same proxy group/node during the test so routing changes are isolated from node changes.
