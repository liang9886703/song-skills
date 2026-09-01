# Hermes Profile Model Switching

Use this reference when a user asks one Hermes profile to use the same model/provider as another profile or agent.

## Workflow

1. Load the protected `hermes-agent` skill first, especially the provider/model and configuration references.
2. Resolve the active profile from `$HERMES_HOME`; do not assume the default `~/.hermes` profile.
3. Inspect the source profile's `config.yaml` for the complete model block, including `model.default`, `model.provider`, `model.base_url`, `model.api_mode` when using a custom OpenAI-compatible endpoint, and the `model.api_key` placeholder/reference. Never print the secret value.
4. Check whether the target profile has the referenced environment variable. If it is absent and the user explicitly requested reuse of the source profile's setup, copy only the matching secret assignment from the source `.env` to the target `.env` without printing it.
5. Use `hermes config set` for every config value; do not hand-edit `config.yaml`.
6. Verify the resulting non-secret values with `hermes config get`.
7. Verify the endpoint using the target profile's credential, preferably `GET /v1/models`, and report only HTTP status and relevant model IDs. Never include the API key in output.
8. Check gateway status before attempting a reload. On macOS, `hermes gateway status` identifies the launchd plist and PID.
9. A gateway process cannot safely restart itself from inside the gateway turn. If `hermes gateway restart` or a direct launchd restart is blocked for that reason, report that the config is saved and verified but requires an external restart. Do not claim the live process has switched until restart/reload is confirmed.

## Important distinction

Updating the profile config changes the next process/session configuration; it does not necessarily change the model already loaded in the current conversation. Preserve the active conversation's model/context and apply the new model after a gateway restart or a supported session-scoped `/model` change.

## Security

- Never print `.env` contents or raw API keys.
- Presence checks should say only whether a variable exists.
- When copying a credential between profiles, do not expose its value, length, or derived form.
- Reuse credentials only after the user explicitly requests matching the other profile's setup.
