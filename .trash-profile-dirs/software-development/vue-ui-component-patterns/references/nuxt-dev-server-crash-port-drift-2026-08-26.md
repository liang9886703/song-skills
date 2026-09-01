# Nuxt Dev Server Crash and Port Drift — blogV2 (2026-08-26)

## Problem

After multiple hot-reload cycles and file edits, the Nuxt dev server crashed with:

```
ENOENT: no such file or directory, open '/Users/songkuakua/Documents/code/Codex-Blog-AI-Chat/blogV2/.nuxt/dev/index.mjs'
```

The `.nuxt/dev/` directory was missing or corrupted. Additionally, the server restarted on a **different port** (3001 instead of 3000) because port 3000 was still occupied by a zombie process.

## Root Cause

1. **Hot-reload corruption**: Vite/Nuxt hot-reload for scoped CSS and module graphs can leave `.nuxt/dev/` in an inconsistent state after many rapid edits, especially when combined with `rm -rf .nuxt` cleanup attempts.
2. **Port drift**: `get-port` automatically falls back to the next available port (3001) when the configured port (8080 or 3000) is occupied. The user may not notice the port change and continues accessing the old port, which now serves a stale or broken instance.

## Fix

1. **Kill all node processes** before restarting:
   ```bash
   lsof -ti :3000 | xargs kill -9 2>/dev/null
   lsof -ti :3001 | xargs kill -9 2>/dev/null
   ```

2. **Full clean restart** (not just hot-reload):
   ```bash
   rm -rf .nuxt
   npm run dev
   ```

3. **Verify the actual port** from the startup logs before browser testing:
   ```
   ➜ Local:    http://127.0.0.1:3001/
   ```

## Pitfalls

- **Don't assume the port is stable** across restarts. Always check the startup log output.
- **Zombie processes survive** `process.kill` in some cases. Use `lsof` to confirm the port is actually free before restarting.
- **`.nuxt` corruption is silent** — the dev server may appear to start successfully but serve 500 errors for all routes. The only fix is a full restart.

## Verification

1. `curl -I http://localhost:<port>/mine` returns 302 (not 500).
2. Browser loads without "ENOENT" or "An error has occurred" pages.
3. `lsof -i :<port>` shows exactly one node process.
