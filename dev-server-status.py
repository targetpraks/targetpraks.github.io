#!/usr/bin/env python3
"""Coolify status checker — checks deployed app URLs, pushes status.json to GitHub Pages.

Checks apps via Host-header requests to 127.0.0.1 (works without Tailscale).

Watchdog behavior: SILENT when healthy. stdout (what the cron delivers to
Discord) is only printed when a service status actually changes — that is the
alert. The status page "Last checked" timestamp is kept fresh by a silent
heartbeat push (output to stderr only) when nothing has changed for
HEARTBEAT_HOURS.
"""

import json
import subprocess
import datetime
import os
import sys
import urllib.request

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(REPO_DIR, "status.json")

# Force a timestamp-refresh push if the pushed status.json is older than this,
# so the status page never shows a stale "Last checked".
HEARTBEAT_HOURS = 2

# All Coolify apps on the Mac mini (LAN IP 100.91.243.82)
APPS = {
    "GSD Dashboard": "http://t5ffr1yc018j0kxd8s8sr4jo.100.91.243.82.sslip.io",
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
    """Check if a URL is reachable via Host header on 127.0.0.1."""
    try:
        host = url.split("//")[1].split("/")[0]
        req = urllib.request.Request("http://127.0.0.1/", method="HEAD")
        req.add_header("Host", host)
        with urllib.request.urlopen(req, timeout=6) as resp:
            return "running"
    except Exception:
        return "stopped"


def last_push_age_hours():
    """Hours since the last commit on main, or None if it can't be determined."""
    try:
        ts = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "main"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if ts:
            last = datetime.datetime.fromisoformat(ts)
            if last.tzinfo is None:
                last = last.replace(tzinfo=datetime.timezone.utc)
            age = datetime.datetime.now(datetime.timezone.utc) - last
            return age.total_seconds() / 3600.0
    except Exception:
        pass
    return None


def main():
    # Sync to origin first so every run starts clean (self-healing against push races)
    os.chdir(REPO_DIR)
    subprocess.run(["git", "fetch", "origin"], capture_output=True, text=True)
    subprocess.run(["git", "reset", "--hard", "origin/main"], capture_output=True, text=True)

    # If Docker/Colima is down, keep the last good status — don't push all-red.
    docker_check = subprocess.run(
        ["docker", "info"], capture_output=True, text=True, timeout=15
    )
    if docker_check.returncode != 0:
        print("Docker/Colima is down — keeping last good status, not pushing", file=sys.stderr)
        sys.exit(0)

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

    # Compare against the last PUSHED state. After the reset --hard above,
    # status.json on disk is exactly what origin/main has.
    old_statuses = {}
    try:
        with open(STATUS_FILE) as f:
            old = json.load(f)
        old_statuses = {s.get("name"): s.get("status") for s in old.get("services", [])}
    except Exception:
        pass

    new_statuses = {s["name"]: s["status"] for s in services}
    changes = [
        f"{name}: {old_statuses.get(name, '?')} -> {new_statuses[name]}"
        for name in new_statuses
        if old_statuses.get(name) != new_statuses[name]
    ]

    age = last_push_age_hours()
    stale = age is None or age > HEARTBEAT_HOURS

    if not changes and not stale:
        # Healthy and nothing changed — stay silent (empty stdout = no Discord message)
        return

    with open(STATUS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    os.chdir(REPO_DIR)
    subprocess.run(["git", "add", "status.json"], check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True)
    if diff.returncode == 0:
        print("No status changes — skipping push", file=sys.stderr)
        return

    if changes:
        msg = f"auto: update dev server status ({running} running, {pending} pending, {stopped} stopped) [{now_jst}]"
    else:
        msg = f"auto: heartbeat status refresh (no status changes) [{now_jst}]"
    subprocess.run(["git", "commit", "-m", msg], check=True)
    push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    if push.returncode == 0:
        if changes:
            # Real status change — this is the alert the watchdog exists to send
            print(
                f"Service status changed ({running} running, {pending} pending, {stopped} stopped): "
                + "; ".join(changes)
            )
        else:
            # Heartbeat refresh — keep Discord silent, note it on stderr only
            print(f"Heartbeat refresh pushed (last push {age:.1f}h ago, no status changes)", file=sys.stderr)
    else:
        print(f"Push failed: {push.stderr}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()