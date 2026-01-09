#!/usr/bin/env bash
set -Eeuo pipefail

IMAGE="ubuntu:22.04"
APP_NAME="balam"
LOG_FILE="build.log"

echo "========================================"
echo " BALAM TUI – Binary Build"
echo "========================================"
echo
echo "This will:"
echo "  • Pull $IMAGE"
echo "  • Install build dependencies"
echo "  • Run PyInstaller"
echo "  • Output a single binary: dist/$APP_NAME"
echo
read -rp "Continue? [y/N]: " CONFIRM
[[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]] || exit 0

echo
echo "Starting build..."
echo "Logging to $LOG_FILE"
echo

docker run --rm -it \
  -v "$PWD:/src" \
  -w /src \
  "$IMAGE" \
  bash <<'EOF' | tee "$LOG_FILE"

set -Eeuo pipefail

echo "[1/6] Updating system"
apt update -y

echo "[2/6] Installing system dependencies"
apt install -y \
  python3 \
  python3-pip \
  python3-venv \
  build-essential \
  patchelf

echo "[3/6] Upgrading pip"
pip3 install --upgrade pip

echo "[4/6] Installing Python dependencies"
pip3 install \
  pyinstaller \
  textual \
  pyyaml

echo "[5/6] Running PyInstaller"
pyinstaller \
  --onefile \
  --name balam \
  --collect-all textual \
  --collect-all yaml \
  --paths=. \
  app.py

echo "[6/6] Build complete"
echo "Binary located at: dist/balam"
echo

read -rp "Build finished. Remain inside container? [y/N]: " CONFIRM
if [[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]]; then
  echo
  echo "Dropping into interactive shell. Type 'exit' to leave."
  exec bash
fi

EOF

echo
echo "Build finished successfully."
