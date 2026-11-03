#!/usr/bin/env python3
"""Prepare daily-report context from ~/daily/YYYY/MM/DD.md files."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Target report date as YYYY-MM-DD. Defaults to the 08:00-based report day.")
    parser.add_argument("--now", help="Current local datetime for testing, as YYYY-MM-DDTHH:MM:SS.")
    parser.add_argument("--day-start-hour", type=int, default=8, help="Hour when a report day starts; default 8.")
    parser.add_argument("--daily-root", default="~/daily", help="Daily report root directory.")
    parser.add_argument("--days", type=int, default=3, help="Number of effective daily files to collect.")
    parser.add_argument("--max-lookback", type=int, default=45, help="Maximum calendar days to scan backward.")
    parser.add_argument("--create-today", action="store_true", help="Create today's file if missing.")
    parser.add_argument("--no-content", action="store_true", help="Do not include report file contents.")
    return parser.parse_args()


def current_datetime(value: str | None) -> dt.datetime:
    if value:
        return dt.datetime.fromisoformat(value)
    return dt.datetime.now()


def infer_report_date(now: dt.datetime, start_hour: int) -> dt.date:
    report_date = now.date()
    if now.hour < start_hour:
        report_date -= dt.timedelta(days=1)
    return report_date


def report_window(day: dt.date, start_hour: int) -> tuple[dt.datetime, dt.datetime]:
    start = dt.datetime.combine(day, dt.time(hour=start_hour))
    return start, start + dt.timedelta(days=1)


def report_path(root: Path, day: dt.date) -> Path:
    return root / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}.md"


def read_text(path: Path, include_content: bool) -> str | None:
    if not include_content:
        return None
    return path.read_text(encoding="utf-8")


def main() -> None:
    args = parse_args()
    if not 0 <= args.day_start_hour <= 23:
        raise SystemExit("--day-start-hour must be between 0 and 23")

    now = current_datetime(args.now)
    target = dt.date.fromisoformat(args.date) if args.date else infer_report_date(now, args.day_start_hour)
    window_start, window_end = report_window(target, args.day_start_hour)
    root = Path(args.daily_root).expanduser()
    today_path = report_path(root, target)

    created_today = False
    if args.create_today and not today_path.exists():
        today_path.parent.mkdir(parents=True, exist_ok=True)
        today_path.touch()
        created_today = True

    reports = []
    cursor = target
    include_content = not args.no_content
    scanned = 0
    while len(reports) < args.days and scanned <= args.max_lookback:
        path = report_path(root, cursor)
        if path.exists():
            reports.append(
                {
                    "date": cursor.isoformat(),
                    "path": str(path),
                    "is_today": cursor == target,
                    "content": read_text(path, include_content),
                }
            )
        cursor -= dt.timedelta(days=1)
        scanned += 1

    payload = {
        "target_date": target.isoformat(),
        "report_window": {
            "start": window_start.isoformat(timespec="minutes"),
            "end": window_end.isoformat(timespec="minutes"),
        },
        "daily_root": str(root),
        "today_path": str(today_path),
        "created_today": created_today,
        "max_lookback": args.max_lookback,
        "reports": reports,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
