#!/usr/bin/env bash
# This script is triggered before every Bash command (PreToolUse).
# It checks whether the command is a 'git commit' and suggests running
# /typo3:code-simplify if there are changed files to commit.

# Read the JSON payload from STDIN. Claude Code passes the tool input here.
payload=$(cat)

# Extract the Bash command from the payload using jq
cmd=$(echo "$payload" | jq -r '.tool_input.command // empty')

# Proceed only if the command is a git commit
if [[ "$cmd" =~ ^git[[:space:]]commit ]]; then
  # Collect a list of all changed file names (staged + unstaged)
  changed=$( (git diff --name-only && git diff --name-only --staged) | sort | uniq )
  # Count how many files were changed
  count=$(echo "$changed" | grep -c . || true)

  if [ "$count" -gt 0 ]; then
    echo "You are committing $count changed file(s):"
    echo "$changed"
    echo "Consider running '/typo3:code-simplify changed goal:full' to simplify them before committing."
  fi
fi
