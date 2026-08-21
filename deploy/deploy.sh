#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"

HOSTNAME="$($PYTHON - "$ROOT/site.json" <<'PY'
import json, sys
from urllib.parse import urlparse
with open(sys.argv[1], encoding="utf-8") as handle:
    url = json.load(handle)["url"]
host = urlparse(url).hostname
if not host:
    raise SystemExit("site.json does not contain a valid URL")
print(host)
PY
)"

DEPLOY_ROOT="${1:-/var/www/$HOSTNAME}"
RELEASE_ID="${RELEASE_ID:-$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || date -u +%Y%m%d%H%M%S)}"

echo "Building site..."
"$PYTHON" "$ROOT/build.py"

echo "Publishing release $RELEASE_ID to $DEPLOY_ROOT..."
"$ROOT/deploy/publish.sh" "$ROOT/dist" "$DEPLOY_ROOT" "$RELEASE_ID"
