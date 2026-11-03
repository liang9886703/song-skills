#!/usr/bin/env bash
# Entrypoint wrapper for scheduled automation (cron or launchd)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$DIR")"
CONFIG_FILE="${1:-$BASE_DIR/examples/config.example.json}"

export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

python3 "$DIR/sync_and_story.py" --config "$CONFIG_FILE"
