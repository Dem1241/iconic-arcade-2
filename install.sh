#!/bin/bash
# Run on the arcade to install or update everything from GitHub:
#   curl -fsSL https://raw.githubusercontent.com/YOUR_USER/iconic-arcade/main/install.sh | bash
set -e

REPO="YOUR_USER/iconic-arcade"
BRANCH="main"
TMP="$(mktemp -d)"

echo "Downloading $REPO ($BRANCH)..."
curl -fsSL "https://github.com/$REPO/archive/refs/heads/$BRANCH.tar.gz" \
  | tar xz --strip-components=1 -C "$TMP"

echo "Installing ports..."
mkdir -p /userdata/roms/ports
cp -r "$TMP"/ports/* /userdata/roms/ports/
chmod +x /userdata/roms/ports/*.sh

rm -rf "$TMP"

# Ask EmulationStation to rescan games (fine if ES isn't running)
curl -fs http://127.0.0.1:1234/reloadgames >/dev/null 2>&1 || true

echo "Done. Look under Ports in the arcade menu."
