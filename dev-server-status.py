#!/usr/bin/env python3
"""Coolify status checker — checks deployed app URLs, pushes status.json to GitHub Pages."""

import json
import subprocess
import datetime
import os
import sys
import urllib.request

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(REPO_DIR, "status.json")

APPS = {
    "Papa Pasta": "http://z51m00l0vfw3erypmwrw7drb.100.91.243.82.sslip.io",
    "Esoteric Command": "http://j626owap98e8hxudwx6amo02.100.91.243.82.sslip.io",
    "INFX Web Media": "http://gc9d19ckjl9o5xbv7ll0iwu6.100.91.243.82.sslip.io",
    "Divorced Dads": "http://x29f5ohoi3vcsb71f3elzfsd.100.91.243.82.sslip.io",
    "Personal Site": "http://p1aei61r7j1jplux91cx54gp.100.91.243.82.sslip.io",
    "ChromaCommand": "http://o3oc10fm2z0gzffee963rmkx.100.91.243.82.sslip.io",
    "SunScout": "http://usolei362859c24hssx15rj8.100.91.243.82.sslip.io",
}

# Apps known to need repo work before they can serve HTTP
PENDING = {"ChromaCommand", "SunScout"}


def check_url(url):
    """Check if a URL is reachable."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=6) as resp:
            return "running"
    except Exception:
        return "stopped"


def main():
    # Sync to origin first so every run starts clean (self-healing against push races)
    os.chdir(REPO_DIR)
    subprocess.run(["git", "fetch", "origin"], capture_output=True, text=True)
    subprocess.run(["git", "reset", "--hard", "origin/main"], capture_output=True, text=True)

    services = []
    running = 0
    pending = 0
    stopped = 0

    for name, url in sorted(APPS.items()):
        status = check_url(url)
        if status == "running":
            running += 1
        elif name in PENDING:
            status = "pending"
            pending += 1
        else:
            stopped += 1
        services.append({"name": name, "url": url, "status": status})

    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    jst_tz = datetime.timezone(datetime.timedelta(hours=2))
    now_jst = datetime.datetime.now(jst_tz).strftime("%Y/%m/%d, %H:%M:%S")

    data = {
        "lastChecked": now_utc,
        "lastCheckedJST": now_jst,
        "services": services,
        "summary": {"running": running, "pending": pending, "stopped": stopped, "total": len(APPS)},
    }

    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Status: {running} running, {pending} pending, {stopped} stopped out of {len(APPS)} services")

    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "status.json"], check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if diff.returncode == 0:
        print("No status changes — skipping push")
    else:
        msg = f"auto: update dev server status ({running} running, {pending} pending, {stopped} stopped) [{now_jst}]"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        if push.returncode == 0:
            print("Pushed status update to GitHub Pages")
        else:
            print(f"Push failed: {push.stderr}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
