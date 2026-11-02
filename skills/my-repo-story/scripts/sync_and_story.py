#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
my-repo-story: Multi-repository safe sync & narrative changelog generator.
General-purpose and desensitized script for tracking engineering momentum across Git repositories.
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime

def run_git(cmd, cwd):
    res = subprocess.run(["git"] + cmd, cwd=cwd, capture_output=True, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def process_repository(repo, since="24 hours ago", dry_run=False):
    name = repo["name"]
    path = os.path.expanduser(repo["path"])
    key = repo.get("key", name)
    
    info = {
        "key": key,
        "name": name,
        "path": path,
        "branch": "unknown",
        "update_status": "PENDING",
        "update_message": "",
        "dirty_files": [],
        "commits": [],
        "sub_components": repo.get("sub_components", [])
    }
    
    if not os.path.exists(path):
        info["update_status"] = "ERROR"
        info["update_message"] = f"Repository path does not exist: {path}"
        return info

    # 1. Current Branch
    rc, stdout, _ = run_git(["branch", "--show-current"], path)
    branch = stdout if rc == 0 and stdout else "DETACHED_HEAD"
    info["branch"] = branch

    # 2. Check for local dirty / uncommitted files
    rc, stdout, _ = run_git(["status", "--porcelain"], path)
    dirty_lines = [l.strip() for l in stdout.splitlines() if l.strip()]
    info["dirty_files"] = dirty_lines

    # 3. Fetch remote
    if not dry_run:
        rc, stdout, stderr = run_git(["fetch", "origin"], path)
        if rc != 0:
            info["update_message"] = f"Fetch failed: {stderr}"
    
    # 4. Pull logic with conflict protection
    if dry_run:
        info["update_status"] = "DRY_RUN"
        info["update_message"] = "Dry run mode enabled; skipped pull."
    elif branch == "DETACHED_HEAD":
        info["update_status"] = "SKIPPED"
        info["update_message"] = "Detached HEAD state; skipped pull."
    elif dirty_lines:
        # Working tree has uncommitted modifications; try fast-forward only
        rc, stdout, stderr = run_git(["pull", "--ff-only"], path)
        if rc == 0:
            info["update_status"] = "SUCCESS"
            info["update_message"] = "Fast-forward pull succeeded despite non-conflicting local files."
        else:
            info["update_status"] = "SKIPPED_DIRTY"
            err_msg = stderr or stdout or "Possible conflict with uncommitted local modifications"
            info["update_message"] = f"Skipped pull to protect {len(dirty_lines)} local changes: {err_msg.splitlines()[0] if err_msg else ''}"
    else:
        # Clean working directory, normal pull
        rc, stdout, stderr = run_git(["pull"], path)
        if rc == 0:
            if "Already up to date" in stdout:
                info["update_status"] = "UP_TO_DATE"
                info["update_message"] = "Already up to date."
            else:
                info["update_status"] = "SUCCESS"
                info["update_message"] = f"Updated successfully: {stdout.splitlines()[0] if stdout else ''}"
        else:
            info["update_status"] = "FAILED"
            info["update_message"] = f"Pull failed: {stderr or stdout}"

    # 5. Extract commits within the specified time window
    git_log_fmt = "%h|%an|%ad|%ar|%s"
    rc, stdout, _ = run_git([
        "log", f"--since={since}", f"--pretty=format:{git_log_fmt}", "--date=iso"
    ], path)
    
    commits = []
    seen_hashes = set()
    if rc == 0 and stdout:
        for line in stdout.splitlines():
            parts = line.split("|", 4)
            if len(parts) == 5 and parts[0] not in seen_hashes:
                seen_hashes.add(parts[0])
                # Fetch commit diff summary
                _, stat_out, _ = run_git(["show", "--stat", "--oneline", parts[0]], path)
                stat_lines = stat_out.splitlines()[1:] if stat_out else []
                stat_summary = stat_lines[-1].strip() if stat_lines else ""
                
                commits.append({
                    "hash": parts[0],
                    "author": parts[1],
                    "date": parts[2],
                    "rel_date": parts[3],
                    "subject": parts[4],
                    "stat_summary": stat_summary
                })

    # If HEAD has no commits and branch has tracking remote, check origin/branch
    if not commits and branch != "DETACHED_HEAD":
        rc, stdout, _ = run_git([
            "log", f"origin/{branch}", f"--since={since}", f"--pretty=format:{git_log_fmt}", "--date=iso"
        ], path)
        if rc == 0 and stdout:
            for line in stdout.splitlines():
                parts = line.split("|", 4)
                if len(parts) == 5 and parts[0] not in seen_hashes:
                    seen_hashes.add(parts[0])
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "rel_date": parts[3],
                        "subject": parts[4] + " (origin)",
                        "stat_summary": ""
                    })

    info["commits"] = commits
    return info

def generate_markdown_report(config, results, since_text):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    scheduler_name = config.get("scheduler_name", "Multi-Repository Update & Story Report")
    
    md = []
    md.append(f"# {scheduler_name} ({date_str})\n")
    md.append(f"**Generated At**: `{now_str}`  ")
    md.append(f"**Time Window**: Past `{since_text}`  ")
    md.append(f"**Schedule**: {config.get('schedule', 'Daily recurring automation')}\n")
    md.append("---\n")

    # 1. Overview Table
    md.append("## 1. Repository Status Overview\n")
    md.append("| Repository | Branch | Status | Working Tree | Commits | Details |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    
    dirty_warnings = []
    total_commits = 0

    for r in results:
        status_icon = "✅" if r["update_status"] in ("SUCCESS", "UP_TO_DATE") else ("⚠️" if "SKIPPED" in r["update_status"] else "❌")
        dirty_icon = f"⚠️ {len(r['dirty_files'])} uncommitted" if r["dirty_files"] else "Clean"
        c_count = len(r["commits"])
        total_commits += c_count
        
        md.append(f"| **{r['key']}** | `{r['branch']}` | {status_icon} {r['update_status']} | {dirty_icon} | **{c_count}** | {r['update_message']} |")
        
        if r["dirty_files"]:
            dirty_warnings.append((r["key"], r["path"], r["dirty_files"]))

    md.append("")

    # Warning section
    if dirty_warnings:
        md.append("> [!WARNING]")
        md.append("> **Local Uncommitted Changes Protected**:")
        for key, p, files in dirty_warnings:
            sample_files = ", ".join(files[:3]) + (f" and {len(files)-3} more" if len(files) > 3 else "")
            md.append(f"> - **`{key}`** (`{p}`): Contains uncommitted modifications (`{sample_files}`). Pull was skipped or restricted to non-conflicting fast-forward to prevent overwriting your local work.")
        md.append("")

    # 2. Detailed Commits & Technical Story
    md.append("## 2. Technical Evolution & Commit Archaeology\n")
    if total_commits == 0:
        md.append(f"No new commits found across tracked branches within the past {since_text}.\n")
    else:
        for r in results:
            if not r["commits"]:
                continue
            md.append(f"### 📦 {r['name']}")
            md.append(f"- **Path**: `{r['path']}`")
            if r["sub_components"]:
                md.append(f"- **Components**: {', '.join(r['sub_components'])}")
            md.append("")
            md.append("| Commit | Author | Time | Commit Message |")
            md.append("| :--- | :--- | :--- | :--- |")
            for c in r["commits"]:
                md.append(f"| `{c['hash']}` | **{c['author']}** | {c['rel_date']} | {c['subject']} |")
            md.append("")

            # Highlight analysis
            md.append("**Change Highlights**:")
            for c in r["commits"][:5]:
                md.append(f"- **`{c['hash']}`** ({c['author']}): {c['subject']}")
                if c.get("stat_summary"):
                    md.append(f"  > `{c['stat_summary']}`")
            md.append("\n---\n")

    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(description="Multi-repository sync & story report generator")
    parser.add_argument("--config", "-c", required=True, help="Path to config.json")
    parser.add_argument("--since", "-s", default="24 hours ago", help="Git log time window (default: '24 hours ago')")
    parser.add_argument("--output-dir", "-o", default=None, help="Custom output directory for reports")
    parser.add_argument("--dry-run", action="store_true", help="Inspect without pulling remote branches")
    args = parser.parse_args()

    config_path = os.path.abspath(args.config)
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config_dir = os.path.dirname(config_path)
    reports_dir = args.output_dir or config.get("paths", {}).get("reports_dir", "./reports")
    if not os.path.isabs(reports_dir):
        reports_dir = os.path.normpath(os.path.join(config_dir, reports_dir))
    os.makedirs(reports_dir, exist_ok=True)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting multi-repo sync & story extraction (window: {args.since})...")
    results = []
    for repo in config.get("repositories", []):
        print(f"--> Processing {repo['name']} ...")
        res = process_repository(repo, since=args.since, dry_run=args.dry_run)
        results.append(res)
        print(f"    Status: {res['update_status']}, Commits: {len(res['commits'])}")

    report_content = generate_markdown_report(config, results, args.since)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    dated_report = os.path.join(reports_dir, f"{date_str}.md")
    latest_report = os.path.join(reports_dir, "latest.md")

    with open(dated_report, "w", encoding="utf-8") as f:
        f.write(report_content)
    with open(latest_report, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Report successfully generated: {dated_report}")

if __name__ == "__main__":
    main()
