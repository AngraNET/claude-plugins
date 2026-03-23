#!/usr/bin/env bash
# start-brain.sh — Launch Claude Code in your PARA Second Brain vault

PARA_DIR="${PARA_DIR:-{para-dir}}"

if [ ! -d "$PARA_DIR" ]; then
  echo "Error: PARA vault not found at $PARA_DIR"
  echo "Set PARA_DIR in your shell profile to override."
  exit 1
fi

cd "$PARA_DIR" || exit 1
exec claude
