# OpenClaw + Hermes model-routing recipe

## Observed configuration pattern

A named OpenClaw agent can have a string model override, for example:

```json5
{
  "id": "sakura_futaba",
  "model": "openai/gpt-5.6-sol",
  "thinkingDefault": "high",
  "models": {
    "openai/gpt-5.6-sol": {
      "agentRuntime": { "id": "codex" }
    }
  }
}
```

The corresponding Hermes profile uses the provider-less model name:

```yaml
model:
  default: gpt-5.6-sol
  provider: openai-codex
agent:
  reasoning_effort: high
```

## Safe update sequence

```bash
# Hermes profile
hermes --profile <profile> config set model.default <model>
hermes --profile <profile> config set agent.reasoning_effort high

# Simple OpenClaw fields; use the correct list index after inspection
openclaw config set 'agents.list[<index>].model' 'provider/model'
openclaw config set 'agents.list[<index>].thinkingDefault' 'high'
openclaw config validate
```

For model-keyed entries, a path containing a model ID can be parsed incorrectly by the dot-path setter. The reliable fallback is:

1. `openclaw config get agents.list`.
2. Parse the returned JSON and modify only the target agent's `model`, `thinkingDefault`, and model-keyed runtime entry.
3. Write a temporary patch object containing the complete `agents.list` array.
4. Apply it with `openclaw config patch --file <patch>`.
5. Run `openclaw config validate`.

Do not copy secrets from the retrieved config into logs or user-facing output.

## Live application check

OpenClaw reports model changes require a restart:

```bash
openclaw gateway restart
openclaw gateway status
```

Success criteria: config validation passes; the target agent reads the requested model and `thinkingDefault`; gateway status reports `Runtime: running` and `Connectivity probe: ok`.

The global/default model shown by `openclaw status` may belong to another agent. Verify the named agent directly. Existing sessions can retain an earlier model; persistent agent defaults normally govern new sessions.
