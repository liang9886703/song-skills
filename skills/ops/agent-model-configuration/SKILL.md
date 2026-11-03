---
name: agent-model-configuration
description: "Use when changing an agent model or reasoning strength."
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [agents, models, reasoning, openclaw, hermes, configuration]
---

# Agent Model Configuration

Use this skill when a named agent/profile needs a persistent model change, reasoning/thinking strength change, or synchronized configuration across Hermes and OpenClaw.

## Core workflow

1. **Identify the actual owner and scope.** Distinguish the Hermes profile from the OpenClaw routed agent. Inspect the active profile list and the agent routing/config before editing. Do not assume that the current chat's default profile is the target agent.
2. **Resolve the exact model ID.** Prefer a model catalog, existing configuration, provider source, or local tests over translating a nickname by guesswork. Preserve the provider prefix in OpenClaw (`provider/model`) and use the provider-specific model name in Hermes.
3. **Configure Hermes with the CLI.** Use the target profile explicitly:
   - `hermes --profile <profile> config set model.default <model>`
   - `hermes --profile <profile> config set agent.reasoning_effort <level>`
   Hermes settings belong in the profile config; do not hand-edit YAML.
4. **Configure OpenClaw with validated config commands.** Set the target agent's model and per-agent thinking default. If the model needs a runtime override, add a model-keyed `agentRuntime` entry with the appropriate runtime (for Codex-backed models, usually `codex`).
5. **Handle punctuation safely.** OpenClaw dot-path setters may split model IDs containing punctuation such as dots or slashes. If a model-keyed nested path fails validation, retrieve `agents.list`, modify only the target entry, and apply the complete `agents.list` through `openclaw config patch --file <validated-patch>`. Never fall back to raw JSON editing when the CLI can validate the write.
6. **Validate before restart.** Verify both Hermes values and run `openclaw config validate`. Check the target agent object rather than relying on the global/default model display.
7. **Restart the owning gateway when required.** OpenClaw reports that model changes require a gateway restart; run `openclaw gateway restart`, then verify `openclaw gateway status` shows the process running and connectivity probe `ok`. Existing sessions may retain their previous model; persistent defaults govern new sessions unless a session-level override is changed.
8. **Report precisely.** State the exact model, reasoning/thinking level, runtime if relevant, validation result, and gateway health. Do not confuse another agent's global/default model with the target agent's model.

## Strength mapping

- Hermes uses `agent.reasoning_effort` with values such as `low`, `medium`, `high`, and `xhigh`.
- OpenClaw uses per-agent `thinkingDefault` with values including `low`, `medium`, `high`, `xhigh`, `adaptive`, and `max`.
- "Reasoning visibility" is separate from reasoning/thinking strength. Do not claim that visible reasoning is enabled merely because the effort level is high.

## Safety and verification

- Never print or copy tokens while inspecting config; redact secrets in outputs.
- Do not modify unrelated agents, global defaults, or channel credentials when the request is agent-scoped.
- Backups produced by the validated config command are useful, but still verify the resulting config and live gateway.
- For the exact OpenClaw/Hermes synchronization recipe and the model-ID punctuation workaround, see `references/openclaw-hermes-model-routing.md`.
