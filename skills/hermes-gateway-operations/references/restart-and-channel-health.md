# Gateway update/restart and channel-health notes

## Deferred restart after update

When working from inside a live messaging gateway, `hermes gateway restart` may be blocked because the process would be stopping itself. Use a deferred external launchd job on macOS:

```bash
mkdir -p "$HOME/.hermes/logs"
launchctl remove ai.hermes.deferred-gateway-restart 2>/dev/null || true
launchctl submit -l ai.hermes.deferred-gateway-restart -- /bin/bash -lc 'sleep 3; hermes gateway restart >> "$HOME/.hermes/logs/restart-after-update.log" 2>&1'
```

Verify afterward:

```bash
sleep 5
hermes gateway status
hermes --version
tail -80 "$HOME/.hermes/logs/restart-after-update.log"
```

Good success signs include a supervised launchd PID, current service definition, and a restart log saying service started.

## Channel health interpretation

- `configured` only means credentials/config are present.
- `connected` in gateway state means the runtime adapter believes it is currently usable.
- `retrying` with an error means configured but not usable until the underlying error is fixed.
- Recent inbound/outbound log lines are stronger evidence than static config.

## Common observations

- Telegram `getUpdates` polling conflicts usually mean another process is polling with the same bot token. Report it as a possible conflict rather than declaring Telegram down if state still says connected.
- Feishu SDK/API compatibility errors after an update should be treated as fixable dependency or adapter drift, not as evidence that Feishu is unavailable in general.

## Privacy

Never print or summarize token values, app secrets, cookies, auth JSON payloads, connection strings, or bot credentials from gateway config/logs.
