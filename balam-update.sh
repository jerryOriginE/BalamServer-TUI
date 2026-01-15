#!/usr/bin/env bash

set -e

BALAM_URL="https://github.com/jerryOriginE/BalamServer-TUI/releases/latest/download/balam"
INSTALL_PATH="/usr/local/bin/balam"
TMP_FILE="$(mktemp)"

echo "Downloading latest balam..."
curl -fsSL "$BALAM_URL" -o "$TMP_FILE"

echo "Setting executable permission..."
chmod +x "$TMP_FILE"

echo "Installing balam to $INSTALL_PATH..."
sudo mv "$TMP_FILE" "$INSTALL_PATH"

echo "balam updated successfully ✔"
echo
echo "Installed version:"
balam --version
