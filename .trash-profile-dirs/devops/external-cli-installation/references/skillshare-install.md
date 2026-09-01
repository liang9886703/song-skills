# `runkids/skillshare` installation reference

## What the repository provides

Repository: `https://github.com/runkids/skillshare`

The project is a standalone Go CLI distributed as release archives, not an npm package. The README documents:

- macOS/Linux installer: `https://raw.githubusercontent.com/runkids/skillshare/main/install.sh`
- Homebrew: `brew install skillshare`
- Default skillshare source directory on macOS/Linux: `~/.config/skillshare/`

The README's runtime-dependency table says the CLI has no Node.js/npm runtime dependency.

## Verified macOS ARM64 installation

At the time of the session, the latest release resolved by the upstream installer was `v0.20.25`. The archive naming pattern was:

```text
https://github.com/runkids/skillshare/releases/download/v0.20.25/skillshare_0.20.25_darwin_arm64.tar.gz
```

The binary was installed and verified at:

```text
/Users/songkuakua/.local/bin/skillshare
```

Verification output confirmed:

```text
skillshare ... v0.20.25
/Users/songkuakua/.local/bin/skillshare
```

## Privilege fallback

The upstream `install.sh` defaults to `/usr/local/bin` and invokes `sudo` when that directory is not writable. In a non-interactive agent terminal, sudo may fail because it cannot read the macOS password. Do not report success after that failure and do not repeat the same sudo command unchanged.

Use a user-level fallback instead:

```bash
bin_dir="$HOME/.local/bin"
mkdir -p "$bin_dir"
# download the matching release archive, extract it, then:
install -m 755 <tmp-dir>/skillshare "$bin_dir/skillshare"
"$bin_dir/skillshare" version
command -v skillshare || true
```

Report the exact binary path and distinguish it from:

- `~/.config/skillshare/` — skillshare's own source/config store
- Hermes profile skills directory — where Hermes loads skills

Do not run `skillshare init` unless initialization was requested separately; installing the executable and initializing its skill store are different operations.
