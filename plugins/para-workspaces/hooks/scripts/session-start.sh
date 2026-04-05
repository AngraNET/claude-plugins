#!/usr/bin/env bash
# PARA Workspaces — Session Start Hook
# Injects a brief PARA status summary into the session context.

SETTINGS_FILE="$HOME/.claude/para-workspaces.local.md"

# If plugin not configured, prompt setup and exit silently
if [ ! -f "$SETTINGS_FILE" ]; then
  echo "PARA Workspaces is installed but not configured. Run /para:setup to get started."
  exit 0
fi

# Read show-dashboard-on-start setting
SHOW_DASHBOARD=$(grep "show-dashboard-on-start:" "$SETTINGS_FILE" | awk '{print $2}' | tr -d '"')
if [ "$SHOW_DASHBOARD" != "true" ]; then
  exit 0
fi

# Read para-dir
PARA_DIR=$(grep "para-dir:" "$SETTINGS_FILE" | awk '{print $2}' | tr -d '"')
PARA_DIR="${PARA_DIR/#\~/$HOME}"

# Check if PARA directory exists
if [ ! -d "$PARA_DIR" ]; then
  echo "PARA directory not found at $PARA_DIR. Run /para:setup to initialize."
  exit 0
fi

# Count items in each bucket
PROJECTS=$(find "$PARA_DIR/01-projects" -name "CLAUDE.md" 2>/dev/null | wc -l | tr -d ' ')
AREAS=$(find "$PARA_DIR/02-areas" -name "CLAUDE.md" 2>/dev/null | wc -l | tr -d ' ')
RESOURCES=$(find "$PARA_DIR/03-resources" -name "CLAUDE.md" 2>/dev/null | wc -l | tr -d ' ')
INBOX=$(find "$PARA_DIR/00-inbox" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

# Count overdue projects (deadline < today)
TODAY=$(date +%Y-%m-%d)
OVERDUE=0
for f in "$PARA_DIR/01-projects/"*/CLAUDE.md; do
  [ -f "$f" ] || continue
  STATUS=$(grep "^status:" "$f" | awk '{print $2}' | tr -d '"')
  DEADLINE=$(grep "^deadline:" "$f" | awk '{print $2}' | tr -d '"')
  if [ "$STATUS" = "active" ] && [ -n "$DEADLINE" ] && [ "$DEADLINE" \< "$TODAY" ]; then
    OVERDUE=$((OVERDUE + 1))
  fi
done

# Build summary message
SUMMARY="PARA Status: $PROJECTS active project(s)"
if [ "$OVERDUE" -gt 0 ]; then
  SUMMARY="$SUMMARY ($OVERDUE overdue)"
fi
SUMMARY="$SUMMARY, $AREAS area(s), $RESOURCES resource(s)"
if [ "$INBOX" -gt 0 ]; then
  SUMMARY="$SUMMARY, $INBOX inbox item(s) pending."
else
  SUMMARY="$SUMMARY, inbox clear."
fi

# Find most urgent project (earliest deadline)
URGENT=""
URGENT_DEADLINE=""
for f in "$PARA_DIR/01-projects/"*/CLAUDE.md; do
  [ -f "$f" ] || continue
  STATUS=$(grep "^status:" "$f" | awk '{print $2}' | tr -d '"')
  [ "$STATUS" != "active" ] && continue
  DEADLINE=$(grep "^deadline:" "$f" | awk '{print $2}' | tr -d '"')
  TITLE=$(grep "^title:" "$f" | sed 's/^title: *//;s/"//g')
  if [ -n "$DEADLINE" ]; then
    if [ -z "$URGENT_DEADLINE" ] || [ "$DEADLINE" \< "$URGENT_DEADLINE" ]; then
      URGENT_DEADLINE="$DEADLINE"
      URGENT="$TITLE"
    fi
  fi
done

if [ -n "$URGENT" ]; then
  SUMMARY="$SUMMARY Most urgent: \"$URGENT\" (deadline: $URGENT_DEADLINE)."
fi

echo "$SUMMARY"
exit 0
