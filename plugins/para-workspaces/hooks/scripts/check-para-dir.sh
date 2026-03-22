#!/usr/bin/env bash
# PARA Workspaces — UserPromptSubmit Hook
# Fast check that PARA directory exists when plugin is active.
# Runs on every user prompt — must be very fast (<50ms).

SETTINGS_FILE="$HOME/.claude/para-workspaces.local.md"

# Exit silently if not configured
[ -f "$SETTINGS_FILE" ] || exit 0

# Read para-dir
PARA_DIR=$(grep "para-dir:" "$SETTINGS_FILE" | awk '{print $2}' | tr -d '"')
PARA_DIR="${PARA_DIR/#\~/$HOME}"

# Exit silently if directory exists
[ -d "$PARA_DIR" ] && exit 0

# Directory missing — warn Claude
echo "Warning: PARA directory not found at $PARA_DIR. If the user asks about PARA, suggest running /para:setup to reinitialize."
exit 0
