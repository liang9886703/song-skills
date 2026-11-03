# Dev Server Port Drift + Stale Process Cleanup (blogV2, 2026-08-26)

## Context
User asked "部署到 8080 了吗，重启一下呢" after the dev server had been restarted multiple times across sessions. Investigation revealed:
- Port 8080 was held by a stale Node process (PID 6402)
- Port 3000 was held by another stale Node process (PID 23374)
- Port 3001 was held by the current dev server (PID 76495)

Nuxt's `get-port` had auto-fallen-back from 8080 → 3000 → 3001 across restarts, leaving a chain of stale processes.

## Fix

```bash
# Check target port
lsof -nP -iTCP:8080 -sTCP:LISTEN
# Kill stale process
kill 6402

# Check fallback ports
lsof -nP -iTCP:3000 -sTCP:LISTEN
kill 23374

# Restart dev server
npm run dev
# Now binds to 8080 successfully
```

## Key lesson

**"Port already in use" is not always obvious.** The process holding the port may be:
- A zombie from a previous `npm run dev` that wasn't cleanly killed
- A crashed Nuxt process that didn't release the port
- A completely different Node app (e.g. another project)

Always `lsof` before assuming the port is free. When the user expects a specific port (documented in AGENTS.md), verify it's actually free before starting the dev server.

## Prevention

Add port documentation to the project's AGENTS.md so agents know the expected port:

```markdown
## 开发服务器
- 端口: 8080
- 启动: `npm run dev`
- 访问: http://localhost:8080
```

When port drift happens, the user notices immediately ("部署到 8080 了吗") — the fix is always to check for and kill stale processes, not to accept the fallback port.
