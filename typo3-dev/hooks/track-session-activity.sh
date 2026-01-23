#!/usr/bin/env bash
# Lightweight session activity tracker
# Updates session tracking files for intelligent code-simplify suggestions
# Runs on Write/Edit operations to track coding activity

SESSION_START_FILE=".git/.code-simplify-session-start"
LAST_ACTIVITY_FILE=".git/.code-simplify-last-activity"

# Skip if not a Git repository
if [ ! -d ".git" ]; then
  exit 0
fi

# Initialize session if needed
if [ ! -f "$SESSION_START_FILE" ]; then
  date +%s > "$SESSION_START_FILE"
fi

# Track last activity
date +%s > "$LAST_ACTIVITY_FILE"

# Check if session has been idle for > 60 minutes - reset session
if [ -f "$LAST_ACTIVITY_FILE" ]; then
  LAST_ACTIVITY=$(cat "$LAST_ACTIVITY_FILE")
  NOW=$(date +%s)
  IDLE_MINUTES=$(( (NOW - LAST_ACTIVITY) / 60 ))

  if [ "$IDLE_MINUTES" -gt 60 ]; then
    # Reset session - new coding session after long break
    date +%s > "$SESSION_START_FILE"
  fi
fi

exit 0
