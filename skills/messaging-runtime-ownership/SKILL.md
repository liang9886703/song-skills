---
name: messaging-runtime-ownership
description: "Use when channel ownership is unclear across runtimes."
version: 1.0.0
metadata:
  hermes:
    tags: [messaging, gateway, ownership, hermes, openclaw, discord]
    related_skills: [messaging-network-diagnostics, hermes-gateway-debugging]
---

# Messaging Runtime Ownership

Use this class-level skill when a channel appears in more than one agent runtime, when a migration may have copied credentials, or when status output from one runtime conflicts with adapter logs from another. The primary goal is to identify the process that actually owns the live channel before making operational changes.

## Ownership proof

1. Enumerate candidate runtimes and their supervisors.
   - Check Hermes profiles and their `config.yaml` files.
   - Check OpenClaw configuration and LaunchAgents only as candidates, not as proof.
   - Inspect process arguments, service state, and channel-specific logs.
2. Match the adapter namespace to the platform event.
   - Hermes evidence includes `hermes_plugins.<platform>_platform.adapter`, `gateway.run`, `inbound message`, `response ready`, and platform send lines.
   - OpenClaw evidence comes from its gateway/channel log namespace and process.
   - The runtime whose adapter log shows the recent inbound event and outbound send is the owner for that incident.
3. Check for credential contention.
   - If both runtimes have the same bot/account credentials, do not start the second runtime merely because its status says configured.
   - A duplicate connection can cause gateway disconnects, polling conflicts, or ambiguous delivery.

## Safe diagnostic sequence

1. Read the original runtime's config and recent logs first.
2. Prove the failing boundary: connection, inbound event, model/provider call, response generation, or outbound send.
3. Only restart the owning runtime, and only after recording the current state.
4. If an alternate runtime was accidentally started, stop it and verify the original runtime's process, adapter connection, inbound handling, and outbound send.
5. Report configuration ownership separately from current connectivity; `configured` and `running` do not prove healthy delivery.

## Discord-specific distinction

For Discord, distinguish the Discord transport from the agent model call:

- `ClientConnectorError` / TLS reset against `discord.com` means Discord transport or proxy trouble.
- A connected Discord adapter followed by `APIConnectionError` at a custom model endpoint means the Discord channel is healthy but the model/provider path is failing.
- Correlate `inbound message` → model/API errors → `response ready` → `Sending response` before blaming Discord.
- Large contexts can make provider failures slow and misleading; record context size and provider endpoint without exposing credentials.

## Pitfalls

- Do not infer ownership from the runtime with the most visible configured accounts.
- Do not launch or restart an alternate gateway before inspecting the original runtime.
- Do not expose bot tokens, API keys, request dumps, or credential contents while comparing configs.
- Do not call a channel recovered until its actual owner shows fresh adapter connection and user-visible send evidence.

## Reference

See `references/hermes-openclaw-discord-ownership.md` for a condensed ownership-proof and incident-correlation recipe.
