---
name: gateway-log-triage
description: "Use when triaging messaging gateway errors from logs."
---

# Gateway Log Triage

Use this when a user reports a generic messaging-surface failure such as "Something went wrong", missing replies, duplicate replies, stale sessions, or platform-specific gateway trouble.

This is a class-level workflow for log-based triage across gateway surfaces. It complements platform-specific docs; do not assume the visible error string is the root cause until logs are correlated by timestamp, platform, chat/session, and message id.

## Core Principle

A user-visible fallback message is not proof of an agent crash. First correlate it with backend evidence:

1. inbound message was received
2. agent turn started
3. tool/model calls ran or failed
4. response became ready
5. platform send attempted or failed

Only call it a backend failure if the correlated turn lacks a normal completion path or has an actual exception on that path.

## Workflow

1. **Anchor the incident**
   - Capture the reported platform, chat/thread, triggering message id if available, and approximate local time.
   - If the user supplied an exact error string, search for it, but do not rely on text search alone; fallback copy may be emitted by another surface or stored only in old transcripts.

2. **Resolve the active profile/home**
   - Prefer the active profile's `$HERMES_HOME/logs`.
   - Also inspect the root/default Hermes logs only when the profile setup may involve multiple gateways or copied platform credentials.

3. **Read the correlated time window**
   - Gateway log: inbound message, routing, response ready, platform send.
   - Agent log: session id, model call, tool calls, turn end reason, exceptions.
   - Error logs: platform reconnects, tracebacks, liveness failures.

4. **Classify findings**
   - **Normal handled error**: tool error is logged, assistant still returns a response. Report the tool-level outcome, not a crash.
   - **Platform send/receive failure**: response ready exists but platform send fails or reconnects. Diagnose platform/network/token layer.
   - **Agent/model failure**: no turn end or exception during model/tool loop. Diagnose provider/tool/session state.
   - **Unrelated background noise**: other platform retries, stale connector errors, or liveness warnings near the same time but not on the incident path. Mention separately, do not blame them.

5. **Report succinctly**
   - State the verdict first.
   - Quote 2-5 high-signal log lines or summarized timestamps.
   - Separate "incident cause" from "other issues noticed".
   - Give the next fix only for the relevant layer.

## Pitfalls

- Do not treat `skill_view` / lookup failures as crashes if the turn ends with `response ready` and platform send.
- Do not blame unrelated platform adapters just because their errors are noisy in `errors.log`.
- Do not conclude "not found in source" means impossible; fallback text may come from a different surface, version, migration archive, or platform wrapper.
- Avoid dumping huge logs into context. Read narrow windows or write small scripts that filter by timestamp/message/session.

## References

- `references/generic-fallback-message.md` — example triage pattern for a generic "Something went wrong" report where the correlated Discord turn completed normally and unrelated Feishu/Telegram noise was present.
