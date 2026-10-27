#!/usr/bin/env python3
import argparse
import glob
import json
import os
import re
import sqlite3
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


HOME = Path.home()
TZ = ZoneInfo("Asia/Shanghai")
START = None
END = None


def in_window_iso(value):
    if not value:
        return False
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(TZ)
    except ValueError:
        return False
    return START <= dt < END


def in_window_ms(value):
    if value is None:
        return False
    dt = datetime.fromtimestamp(int(value) / 1000, tz=ZoneInfo("UTC")).astimezone(TZ)
    return START <= dt < END


def local_iso_from_ms(value):
    return datetime.fromtimestamp(int(value) / 1000, tz=ZoneInfo("UTC")).astimezone(TZ).isoformat(timespec="minutes")


def local_iso(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(TZ).isoformat(timespec="minutes")


def text_from_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks = []
        for item in content:
            if isinstance(item, str):
                chunks.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if isinstance(text, str):
                    chunks.append(text)
        return "\n".join(chunks)
    if isinstance(content, dict):
        return str(content.get("text") or content.get("content") or "")
    return ""


def clean_text(text):
    text = text or ""
    text = re.sub(r"<environment_context>.*?</environment_context>", "", text, flags=re.S)
    text = re.sub(r"<local-command-caveat>.*?</local-command-caveat>", "", text, flags=re.S)
    text = re.sub(r"<command-name>.*?</command-args>", "", text, flags=re.S)
    text = re.sub(r"<skill>.*?</skill>", "", text, flags=re.S)
    text = re.sub(r"<[^>\n]{1,80}>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def useful(text):
    text = clean_text(text)
    if not text:
        return False
    lowered = text.lower()
    skips = [
        "environment_context",
        "local-command-caveat",
        "permissions instructions",
        "collaboration_mode",
        "apps_instructions",
        "skills_instructions",
        "plugins_instructions",
        "current_date",
        "filesystem sandboxing",
        "approval assessment",
        "treat the transcript",
    ]
    return not any(s in lowered for s in skips)


def truncate(text, n=900):
    text = clean_text(text)
    if len(text) <= n:
        return text
    return text[:n].rstrip() + " ..."


def collect_codex():
    files = []
    day = START.date()
    while day <= END.date():
        files.extend(glob.glob(str(HOME / ".codex" / "sessions" / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}" / "*.jsonl")))
        day += timedelta(days=1)
    sessions = []
    for path in sorted(files):
        meta = {}
        items = []
        started = None
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = rec.get("timestamp")
                if ts and in_window_iso(ts) and started is None:
                    started = ts
                if rec.get("type") == "session_meta":
                    meta = rec.get("payload", {})
                if not ts or not in_window_iso(ts):
                    continue
                payload = rec.get("payload", {})
                if rec.get("type") == "response_item" and payload.get("type") == "message":
                    role = payload.get("role")
                    text = text_from_content(payload.get("content"))
                    if useful(text):
                        items.append((local_iso(ts), role, truncate(text)))
        if items:
            sessions.append({
                "source": "codex",
                "path": path,
                "cwd": meta.get("cwd", ""),
                "start": local_iso(started) if started else "",
                "items": items,
            })
    return sessions


def collect_claude():
    paths = glob.glob(str(HOME / ".claude" / "projects" / "**" / "*.jsonl"), recursive=True)
    sessions = []
    for path in sorted(paths):
        items = []
        cwd = ""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ts = rec.get("timestamp")
                if not ts or not in_window_iso(ts) or rec.get("isMeta"):
                    continue
                cwd = cwd or rec.get("cwd", "")
                msg = rec.get("message") or {}
                role = msg.get("role") or rec.get("type")
                text = text_from_content(msg.get("content"))
                if useful(text):
                    items.append((local_iso(ts), role, truncate(text)))
        if items:
            sessions.append({
                "source": "claude",
                "path": path,
                "cwd": cwd,
                "items": items,
            })
    return sessions


def collect_opencode():
    db = HOME / ".local" / "share" / "opencode" / "opencode.db"
    if not db.exists():
        return []
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sessions = {}
    for row in cur.execute("select * from session order by time_created"):
        if in_window_ms(row["time_created"]) or in_window_ms(row["time_updated"]):
            sessions[row["id"]] = {
                "source": "opencode",
                "id": row["id"],
                "title": row["title"],
                "directory": row["directory"],
                "start": local_iso_from_ms(row["time_created"]),
                "updated": local_iso_from_ms(row["time_updated"]),
                "items": [],
            }

    if not sessions:
        return []

    q_marks = ",".join("?" for _ in sessions)
    message_meta = {}
    for row in cur.execute(f"select * from message where session_id in ({q_marks}) order by time_created", tuple(sessions)):
        data = json.loads(row["data"])
        if in_window_ms(row["time_created"]):
            message_meta[row["id"]] = data.get("role", "")

    for row in cur.execute(f"select * from part where session_id in ({q_marks}) order by time_created", tuple(sessions)):
        if not in_window_ms(row["time_created"]):
            continue
        try:
            data = json.loads(row["data"])
        except json.JSONDecodeError:
            continue
        typ = data.get("type")
        text = ""
        if typ == "text":
            text = data.get("text", "")
        elif typ == "tool":
            state = data.get("state") or {}
            inp = state.get("input") or {}
            out = state.get("output") or ""
            text = f"tool:{data.get('tool')} input={inp} output={str(out)[:300]}"
        if useful(text):
            sessions[row["session_id"]]["items"].append(
                (local_iso_from_ms(row["time_created"]), message_meta.get(row["message_id"], ""), truncate(text))
            )
    conn.close()
    return [s for s in sessions.values() if s["items"]]


def compact_items(items):
    users = []
    assistants = []
    for ts, role, text in items:
        if text.startswith("# AGENTS.md instructions"):
            continue
        if text.startswith("{\"agent_path\""):
            continue
        if text.startswith("请阅读 .agents/skills/runner-prod-analyze/log-download.md"):
            continue
        if "\"outcome\":\"allow\"" in text or "\"risk_level\"" in text:
            continue
        if role == "user":
            users.append((ts, text))
        elif role == "assistant":
            if not text.startswith("tool:"):
                assistants.append((ts, text))
    compact = []
    for ts, text in users[:4]:
        compact.append((ts, "user", truncate(text, 520)))
    if len(users) > 4:
        compact.append((users[-1][0], "user", f"... 另有 {len(users) - 4} 条用户消息，最后一条：{truncate(users[-1][1], 420)}"))
    if assistants:
        compact.append((assistants[-1][0], "assistant-final", truncate(assistants[-1][1], 650)))
    return compact


def print_sessions(name, sessions):
    print(f"\n## {name} ({len(sessions)})")
    for s in sessions:
        citems = compact_items(s["items"])
        if not citems:
            continue
        label = s.get("title") or os.path.basename(s.get("path", s.get("id", "")))
        cwd = s.get("cwd") or s.get("directory") or ""
        print(f"\n### {label}")
        if s.get("start"):
            print(f"- start: {s['start']}")
        if s.get("updated"):
            print(f"- updated: {s['updated']}")
        if cwd:
            print(f"- cwd: {cwd}")
        for ts, role, text in citems:
            print(f"- {ts} [{role}] {text}")


def infer_report_date(now):
    if now.timetz() < time(8, 0, tzinfo=now.tzinfo):
        return now.date() - timedelta(days=1)
    return now.date()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Collect compact Codex, Claude Code, and OpenCode conversations for a daily report window."
    )
    parser.add_argument("--date", help="Report date in YYYY-MM-DD. Window is 08:00 on date to 08:00 next day.")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="IANA timezone, default: Asia/Shanghai.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    TZ = ZoneInfo(args.timezone)
    if args.date:
        report_date = datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        report_date = infer_report_date(datetime.now(TZ))
    START = datetime.combine(report_date, time(8, 0), tzinfo=TZ)
    END = START + timedelta(days=1)
    print(f"# Agent context {START.isoformat(timespec='minutes')} -> {END.isoformat(timespec='minutes')}")
    print_sessions("Codex", collect_codex())
    print_sessions("Claude Code", collect_claude())
    print_sessions("OpenCode", collect_opencode())
