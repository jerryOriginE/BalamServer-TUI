#!/bin/bash
set -Eeuo pipefail

echo
echo "Running PyInstaller build..."
echo

pyinstaller \
  --onefile \
  --name balam \
  --collect-all textual \
  --collect-all yaml \
  --paths=. \
  app.py

echo
echo "Build complete."
echo "Binary located at: dist/balam"
echo

exit

