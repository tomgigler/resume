#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ] || [ "$#" -gt 3 ]; then
    echo "Usage: $0 <built-site-dir> <deploy-root> <release-id>" >&2
    exit 2
fi

SOURCE_DIR="$(cd "$1" && pwd)"
DEPLOY_ROOT="$2"
RELEASE_ID="$3"
RELEASES_DIR="$DEPLOY_ROOT/releases"
RELEASE_DIR="$RELEASES_DIR/$RELEASE_ID"

if [ ! -f "$SOURCE_DIR/index.html" ]; then
    echo "ERROR: $SOURCE_DIR does not look like a built site (index.html missing)" >&2
    exit 1
fi

mkdir -p "$RELEASES_DIR"

if [ -e "$RELEASE_DIR" ]; then
    echo "Release already exists; reusing $RELEASE_DIR"
else
    TMP_DIR="$RELEASES_DIR/.${RELEASE_ID}.tmp.$$"
    trap 'rm -rf "$TMP_DIR"' EXIT

    mkdir "$TMP_DIR"
    cp -a "$SOURCE_DIR/." "$TMP_DIR/"
    mv "$TMP_DIR" "$RELEASE_DIR"
    trap - EXIT
fi

LINK_TMP="$DEPLOY_ROOT/.current.tmp.$$"
ln -s "releases/$RELEASE_ID" "$LINK_TMP"
mv -Tf "$LINK_TMP" "$DEPLOY_ROOT/current"

echo "Published $RELEASE_ID"
echo "Current release: $(readlink -f "$DEPLOY_ROOT/current")"
