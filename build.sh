#!/usr/bin/env bash
set -Eeuo pipefail

IMAGE="ubuntu:22.04"
CONTAINER="balam-tui-build"
APP_NAME="balam"

echo "========================================"
echo " BALAM TUI – Binary Build"
echo "========================================"
echo
echo "Container : $CONTAINER"
echo "Base image: $IMAGE"
echo "Output    : dist/$APP_NAME"
echo

read -rp "Continue? [y/N]: " CONFIRM
[[ "$CONFIRM" == "y" || "$CONFIRM" == "Y" ]] || exit 0

echo 'starting container...'
docker exec -i "$CONTAINER" /bin/bash < ./binary_build.sh
