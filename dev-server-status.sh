#!/bin/bash
# Dev server status checker — runs on Mac mini, pushes status.json to GitHub Pages
# Checks all dev server ports and writes results to targetpraks.github.io repo

set -euo pipefail

REPO_DIR="/Volumes/Hiksemi 1TB/DevMini/targetpraks.github.io"
STATUS_FILE="$REPO_DIR/status.json"
PORTS=(3001 3002 3003 3004 3005 8001 5173 8788)

# Array of (port, name, stack, description)
declare -A PORT_NAMES
PORT_NAMES[3001]="Papa Pasta"
PORT_NAMES[3002]="Esoteric Command"
PORT_NAMES[3003]="INFX Web Media"
PORT_NAMES[3004]="ChromaCommand Dashboard"
PORT_NAMES[3005]="ChromaCommand tRPC API"
PORT_NAMES[8001]="Divorced Dads"
PORT_NAMES[5173]="SunScout App"
PORT_NAMES[8788]="SunScout Express API"

# Build JSON
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
JST_TIME=$(TZ="Africa/Johannesburg" date +"%Y/%m/%d, %H:%M:%S")

RUNNING=0
STOPPED=0

echo "{"
echo "  \"lastChecked\": \"$TIMESTAMP\","
echo "  \"lastCheckedJST\": \"$JST_TIME\","
echo "  \"services\": ["

FIRST=true
for port in "${PORTS[@]}"; do
  # Check if port is listening
  if nc -z -w 2 localhost "$port" 2>/dev/null; then
    STATUS="running"
    RUNNING=$((RUNNING + 1))
  else
    STATUS="stopped"
    STOPPED=$((STOPPED + 1))
  fi

  NAME="${PORT_NAMES[$port]}"

  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo ","
  fi
  printf '    {"port": %s, "name": "%s", "status": "%s"}' "$port" "$NAME" "$STATUS"
done

echo ""
echo "  ],"
echo "  \"summary\": {\"running\": $RUNNING, \"stopped\": $STOPPED, \"total\": ${#PORTS[@]}}"
echo "}" > "$STATUS_FILE"

# Rebuild the JSON properly (the above was just for display, let's do it right)
python3 -c "
import json, subprocess, datetime

ports = {
    3001: 'Papa Pasta',
    3002: 'Esoteric Command',
    3003: 'INFX Web Media',
    3004: 'ChromaCommand Dashboard',
    3005: 'ChromaCommand tRPC API',
    8001: 'Divorced Dads',
    5173: 'SunScout App',
    8788: 'SunScout Express API',
}

services = []
running = 0
stopped = 0

for port, name in sorted(ports.items()):
    try:
        subprocess.run(['nc', '-z', '-w', '2', 'localhost', str(port)],
                      capture_output=True, timeout=3, check=True)
        status = 'running'
        running += 1
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        status = 'stopped'
        stopped += 1
    services.append({'port': port, 'name': name, 'status': status})

now_utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2))).strftime('%Y/%m/%d, %H:%M:%S')

data = {
    'lastChecked': now_utc,
    'lastCheckedJST': now_jst,
    'services': services,
    'summary': {'running': running, 'stopped': stopped, 'total': len(ports)}
}

with open('$STATUS_FILE', 'w') as f:
    json.dump(data, f, indent=2)

print(f'Status: {running} running, {stopped} stopped out of {len(ports)} services')
" 2>&1

# Git commit and push if status changed
cd "$REPO_DIR"
git add status.json
if git diff --cached --quiet; then
  echo "No status changes — skipping push"
else
  git commit -m "auto: update dev server status ($RUNNING running, $STOPPED stopped) [$JST_TIME]"
  git push origin main 2>&1
  echo "Pushed status update to GitHub Pages"
fi