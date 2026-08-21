#!/usr/bin/env python3
"""Render an Apache vhost from site.json."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
HOSTNAME = re.compile(r"^[A-Za-z0-9.-]+$")

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--site", type=Path, default=ROOT / "site.json")
parser.add_argument("--document-root", default="")
args = parser.parse_args()

with args.site.open(encoding="utf-8") as handle:
    site = json.load(handle)

host = urlparse(site["url"]).hostname or ""
if not HOSTNAME.fullmatch(host):
    raise SystemExit("site.json contains an invalid hostname")

document_root = args.document_root or f"/var/www/{host}"

print(f"""<VirtualHost *:80>
    ServerName {host}
    DocumentRoot {document_root}

    <Directory {document_root}>
        Options -Indexes
        AllowOverride None
        Require all granted
    </Directory>

    ErrorDocument 404 /404.html

    ErrorLog ${{APACHE_LOG_DIR}}/{host}-error.log
    CustomLog ${{APACHE_LOG_DIR}}/{host}-access.log combined
</VirtualHost>""")
