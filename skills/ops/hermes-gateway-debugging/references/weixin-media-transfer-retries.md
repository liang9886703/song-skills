# Weixin media transfer retry debugging note

Use this when a Hermes Weixin/WeChat gateway session receives text but media links/images/files intermittently fail with `Cannot connect to host ... ssl:default [None]` or similar transient CDN/API connection errors.

## Tight loop

1. Inspect gateway logs for the failing boundary:
   - `gateway.platforms.weixin: image download failed: Cannot connect to host novac2c.cdn.weixin.qq.com:443 ...`
   - `gateway.platforms.weixin: send chunk failed ...`
   - `gateway.platforms.weixin: poll error ... ilinkai.weixin.qq.com ...`
2. Distinguish:
   - long-poll/API startup errors (`ilinkai.weixin.qq.com`) from
   - media CDN transfer errors (`novac2c.cdn.weixin.qq.com/c2c`).
3. If curl/aiohttp succeeds on retry or later logs show Weixin reconnecting, treat the original failure as transient network instability, not bad credentials.

## Fix pattern

For transient Weixin media transfer failures, patch the media boundary rather than the gateway loop:

- Add bounded retries around `_download_bytes()` for inbound media downloads.
- Add bounded retries around `_upload_ciphertext()` for outbound media uploads.
- Preserve `asyncio.wait_for()` around each attempt; do not reintroduce aiohttp `timeout=` kwargs, because those previously caused cross-loop `Timeout context manager should be used inside a task` errors in cron/standalone sends.
- Always re-raise `asyncio.CancelledError` immediately.

## Regression tests

Add tests that use stub sessions where the first `get()` or `post()` raises a transient exception and the second succeeds. Assert:

- the helper returns the successful bytes/encrypted param,
- the session was called twice,
- `asyncio.sleep()` was awaited with the retry delay.

## Verification

Run the Weixin focused suite with the project wrapper:

```bash
scripts/run_tests.sh tests/gateway/test_weixin.py tests/gateway/test_weixin_typing.py -q
```

If the running gateway was affected, restart it and confirm logs contain:

- `Connecting to weixin...`
- `[Weixin] Connected account=... base=https://ilinkai.weixin.qq.com`
- `✓ weixin connected`
