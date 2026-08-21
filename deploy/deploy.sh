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

DEST_DIR="${1:-/var/www/$HOSTNAME}"

echo "Building site..."
"$PYTHON" "$ROOT/build.py"

echo "Deploying to $DEST_DIR..."
sudo mkdir -p "$DEST_DIR"
sudo rsync -a --delete "$ROOT/dist/" "$DEST_DIR/"
sudo chown -R root:www-data "$DEST_DIR"
sudo find "$DEST_DIR" -type d -exec chmod 755 {} \;
sudo find "$DEST_DIR" -type f -exec chmod 644 {} \;

echo "Deployment complete: $DEST_DIR"
