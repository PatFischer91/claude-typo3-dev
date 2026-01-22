#!/usr/bin/env bash
# Smart Code Simplifier Hook
# Intelligently suggests or asks about code simplification based on context
# Triggers: Pre-commit + session-based (after longer coding sessions)
# Philosophy: Helpful, not annoying

LAST_RUN_FILE=".git/.code-simplify-last-run"
SESSION_START_FILE=".git/.code-simplify-session-start"
LAST_ACTIVITY_FILE=".git/.code-simplify-last-activity"
NOW=$(date +%s)

# Ensure Git directory exists
if [ ! -d ".git" ]; then
  # Not a Git repository - skip hook
  exit 0
fi

# Initialize session tracking
if [ ! -f "$SESSION_START_FILE" ]; then
  echo "$NOW" > "$SESSION_START_FILE"
fi

# Update last activity
echo "$NOW" > "$LAST_ACTIVITY_FILE"

# Get context
SESSION_START=$(cat "$SESSION_START_FILE" 2>/dev/null || echo "$NOW")
LAST_RUN=$(cat "$LAST_RUN_FILE" 2>/dev/null || echo "0")
SESSION_DURATION=$(( (NOW - SESSION_START) / 60 )) # minutes
TIME_SINCE_LAST=$(( (NOW - LAST_RUN) / 60 )) # minutes

# Count changed files (staged + unstaged, PHP files only for relevance)
CHANGED_PHP=$(( $(git diff --name-only '*.php' 2>/dev/null | wc -l) + $(git diff --name-only --staged '*.php' 2>/dev/null | wc -l) ))
CHANGED_ALL=$(( $(git diff --name-only 2>/dev/null | wc -l) + $(git diff --name-only --staged 2>/dev/null | wc -l) ))

# Decision logic: Never prompt if recently run
if [ "$TIME_SINCE_LAST" -lt 15 ]; then
  # Recently ran code-simplify - no prompt (cooldown period)
  exit 0
fi

# Too few changes - no point suggesting
if [ "$CHANGED_ALL" -lt 5 ]; then
  exit 0
fi

# Detect trigger type from payload
payload=$(cat)
cmd=$(echo "$payload" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Pre-commit trigger (always suggest if significant changes)
if [[ "$cmd" =~ ^git[[:space:]]commit ]]; then
  if [ "$CHANGED_PHP" -gt 0 ]; then
    echo ""
    echo "💡 Code Quality Check"
    echo "   You're committing $CHANGED_ALL file(s) ($CHANGED_PHP PHP)."
    echo "   Consider: /typo3:code-simplify"
    echo "   (Keeps code clean and reviewable)"
    echo ""
  fi
  exit 0
fi

# Session-based trigger - intelligent thresholds
if [ "$SESSION_DURATION" -ge 30 ]; then
  # Long session + many changes = stronger suggestion
  if [ "$CHANGED_ALL" -ge 20 ] || [ "$SESSION_DURATION" -ge 45 ]; then
    echo ""
    echo "🔍 Code Simplification Check"
    echo "   Session: ${SESSION_DURATION}min | Changed: $CHANGED_ALL files ($CHANGED_PHP PHP)"
    echo "   Consider running: /typo3:code-simplify"
    echo "   (Behavior-preserving refactoring and cleanup)"
    echo ""
  elif [ "$CHANGED_ALL" -ge 10 ]; then
    # Moderate changes - gentle reminder
    echo "💡 Tip: Code simplify available after $CHANGED_ALL changes in ${SESSION_DURATION}min session."
  fi
fi

exit 0
