# Hooks Testing & Verification

This document explains how the hooks work and how to verify they function correctly within Claude Code.

## Important: ${CLAUDE_PLUGIN_ROOT} is Automatic!

**Users don't need to configure anything!** The `${CLAUDE_PLUGIN_ROOT}` variable is **automatically set by Claude Code** when the plugin is loaded. No user action required.

**How it works:**
- User installs plugin: `claude plugin install ./typo3-dev`
- Claude copies to: `~/.claude/plugins/typo3-dev/`
- Claude automatically sets: `CLAUDE_PLUGIN_ROOT=~/.claude/plugins/typo3-dev`
- Hooks reference scripts: `${CLAUDE_PLUGIN_ROOT}/hooks/script.sh`

## Hook Files Overview

### 1. `load-development-standards.sh`
**Trigger:** SessionStart
**Purpose:** Loads TYPO3 coding guidelines from `development_standards.md`
**Output:** Full guidelines text sent as prompt to Claude

### 2. `track-session-activity.sh`
**Trigger:** SessionStart
**Purpose:** Initializes session tracking for intelligent code-simplify suggestions
**Creates Files:**
- `.git/.code-simplify-session-start` - Session start timestamp
- `.git/.code-simplify-last-activity` - Last activity timestamp

### 3. `smart-code-simplify.sh`
**Trigger:** PreToolUse (on Bash commands, especially `git commit`)
**Purpose:** Suggests running `/typo3:code-simplify` when appropriate
**Logic:**
- Suggests before commits with 5+ changed files
- Suggests during long sessions (30+ min) with many changes
- Has 15-minute cooldown between suggestions
- Tracks via `.git/.code-simplify-last-run`

## Tracking Files Location

All tracking files are stored in your project's `.git/` directory:

```
your-project/.git/
├── .code-simplify-session-start   # When current session started
├── .code-simplify-last-activity   # Last Write/Edit operation
└── .code-simplify-last-run        # Last time code-simplify was suggested
```

These files contain Unix timestamps (seconds since epoch).

## How to Verify in Claude Code

### 1. Check Session Start Hook

When you start a new Claude session with the plugin active, you should see the TYPO3 guidelines loaded. Look for output like:

```
Apply the following TYPO3 Coding Guidelines throughout this session:

# PHP/TYPO3 Development Standards
...
```

### 2. Check Tracking Files Created

After starting a session, check if tracking files exist:

```bash
ls -la .git/.code-simplify-*
```

You should see two files with current timestamps.

### 3. Check Code Simplify Suggestions

When you commit PHP files, you should see a suggestion like:

```
💡 Code Quality Check
   You're committing 8 file(s) (5 PHP).
   Consider: /typo3:code-simplify
   (Keeps code clean and reviewable)
```

### 4. Decode Timestamps

To see human-readable dates from tracking files:

```bash
# Session start time
date -d @$(cat .git/.code-simplify-session-start) '+%Y-%m-%d %H:%M:%S'

# Last activity
date -d @$(cat .git/.code-simplify-last-activity) '+%Y-%m-%d %H:%M:%S'

# Session duration in minutes
echo $(( ($(date +%s) - $(cat .git/.code-simplify-session-start)) / 60 ))
```

## Manual Testing

### Test Scripts Directly

From your project directory (where `.git/` exists):

```bash
# Test load-development-standards.sh
~/.claude/plugins/typo3-dev/hooks/load-development-standards.sh | head -20

# Test track-session-activity.sh
~/.claude/plugins/typo3-dev/hooks/track-session-activity.sh
ls -la .git/.code-simplify-*

# Test smart-code-simplify.sh with git commit
echo '{"tool_input":{"command":"git commit -m test"}}' | ~/.claude/plugins/typo3-dev/hooks/smart-code-simplify.sh

# Reset tracking (force fresh session)
rm .git/.code-simplify-*
```

### Test During Plugin Development

From the plugin repository root:

```bash
# Test scripts
./typo3-dev/hooks/load-development-standards.sh | head -20
./typo3-dev/hooks/track-session-activity.sh
ls -la .git/.code-simplify-*
```

## Troubleshooting

### SessionStart hook error

**Cause:** Script cannot find or execute load-development-standards.sh
**Check:**
```bash
# Verify plugin is installed
ls ~/.claude/plugins/typo3-dev/hooks/

# Verify script is executable
ls -l ~/.claude/plugins/typo3-dev/hooks/load-development-standards.sh

# Test script manually
~/.claude/plugins/typo3-dev/hooks/load-development-standards.sh
```

### No tracking files created

**Cause:** Not in a Git repository
**Solution:** Hooks only work in directories with `.git/` folder

Check:
```bash
# Are you in a git repo?
git rev-parse --show-toplevel
```

### No code-simplify suggestions

**Possible reasons:**
1. Recently suggested (< 15 min cooldown)
2. Too few changes (< 5 files)
3. Short session (< 30 min) with moderate changes

Check cooldown status:
```bash
if [ -f .git/.code-simplify-last-run ]; then
  LAST_RUN=$(cat .git/.code-simplify-last-run)
  NOW=$(date +%s)
  MINUTES_AGO=$(( (NOW - LAST_RUN) / 60 ))
  echo "Last suggestion: $MINUTES_AGO minutes ago"
else
  echo "Never suggested (no cooldown)"
fi
```

## Understanding ${CLAUDE_PLUGIN_ROOT}

The `${CLAUDE_PLUGIN_ROOT}` environment variable points to the plugin's installation directory.

**Example:**
```json
{
  "type": "command",
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/track-session-activity.sh"
}
```

**Expands to:**
```bash
~/.claude/plugins/typo3-dev/hooks/track-session-activity.sh
```

**Why it's needed:**
- Scripts are in the plugin directory: `~/.claude/plugins/typo3-dev/hooks/`
- Scripts are executed in the user's project directory: `/path/to/user/project/`
- Without `${CLAUDE_PLUGIN_ROOT}`, relative paths wouldn't work
- With `${CLAUDE_PLUGIN_ROOT}`, the plugin works for all users automatically

## Hook Lifecycle

```
Session Start (once)
├── load-development-standards.sh → Load coding guidelines
└── track-session-activity.sh     → Initialize session timestamp

Every Bash Command (PreToolUse)
└── smart-code-simplify.sh        → Check if suggestion needed
```

## Technical Details

**Script Execution Context:**
- Working Directory: User's project root
- Plugin Scripts: `${CLAUDE_PLUGIN_ROOT}/hooks/`
- Tracking Files: `${PWD}/.git/.code-simplify-*`

**Script Self-Location:**
Scripts use `${BASH_SOURCE[0]}` to find adjacent files:
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STANDARDS_FILE="$SCRIPT_DIR/development_standards.md"
```

This ensures `load-development-standards.sh` can find `development_standards.md` regardless of where it's called from.
