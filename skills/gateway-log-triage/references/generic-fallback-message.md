# Generic fallback message triage example

## Situation

A user reported a visible fallback message:

```text
⚠️ Something went wrong while processing your request. Please try again, or use /new to start a fresh session.
```

The nearby conversation involved looking up missing skills (`khazix-writer`, `hv-analysis`) from a Discord DM.

## What to correlate

For the reported turn, compare:

- `gateway.log`: inbound message, `response ready`, platform send line
- `agent.log`: session id, model calls, tool calls, `Turn ended`
- `errors.log` / `gateway.error.log`: nearby tracebacks or platform reconnects
- exact fallback text in source/logs, but treat absence as inconclusive

## Example finding pattern

High-signal lines showed the suspected `hv-analysis` request completed normally:

```text
14:59:41 inbound message ... msg='hv-analysis 呢'
14:59:49 tool skill_view failed: Skill 'hv-analysis' not found.
14:59:56 Turn ended: reason=text_response(...)
14:59:56 response ready ... response=258 chars
14:59:56 [Discord] Sending response ...
```

That means the missing skill was a handled lookup failure, not an agent crash.

Nearby noisy errors were unrelated to that Discord turn:

```text
[Feishu] Failed to connect: Client.__init__() got an unexpected keyword argument 'extra_ua_tags'
[Telegram] SSLV3_ALERT_HANDSHAKE_FAILURE ... polling restarted after network error
```

These should be reported under "other issues noticed", not as the cause of the visible Discord result.

## Reporting pattern

Use a short verdict-first response:

1. "The correlated Discord turn completed normally; this was not a backend crash."
2. Summarize the exact correlated timestamps.
3. Explain the handled error (`skill_view` not found) separately from unrelated platform noise.
4. If there is a real noisy issue, identify its layer (e.g. Feishu SDK/plugin version mismatch, Telegram transient TLS/proxy issue) without blaming it for the incident.

## Durable lesson

Generic fallback text is only a symptom. The durable debugging pattern is correlation by platform + chat/session + timestamp + message id, then classification of the exact failure layer.
