# Hermes/OpenClaw Discord ownership recipe

Use this when both Hermes and OpenClaw appear to have Discord configuration.

## Proof checklist

- Inspect every Hermes profile's `config.yaml` for a Discord section; the active profile may differ from the default profile.
- Inspect Hermes profile gateway logs for `hermes_plugins.discord_platform.adapter`, `Connected as`, `inbound message`, `response ready`, and `[Discord] Sending response`.
- Inspect OpenClaw status/logs only as a competing candidate. A configured OpenClaw account is not ownership evidence.
- Compare process/service arguments, but never print tokens or credential files.

## Incident classification

- Discord adapter connection error: `Cannot connect to host discord.com:443`, TLS handshake reset, or proxy errors.
- Model/provider error after a confirmed Discord inbound event: `APIConnectionError` with a custom provider endpoint. Treat Discord as healthy until outbound evidence disproves it.
- Healthy delivery: the same owner's logs show the sequence `inbound message` → `response ready` → `Sending response`.

## Safe recovery

Do not start the candidate runtime during diagnosis. If it was started by mistake, stop it, then re-check the original owner's adapter connection and fresh send evidence. Restart only the proven owner.

## Context-size clue

When model calls fail slowly and the log reports hundreds of thousands of context tokens, record the provider/model and context size. Prefer a fresh session or a known-good model/provider before changing Discord routing.
