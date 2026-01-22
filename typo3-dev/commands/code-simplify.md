---
description: >
  Run the TYPO3 code-simplifier agent. Defaults to changed files but supports interactive scope selection:
  changed files, specific directory, specific files, or whole repository. Also supports interactive goals selection:
  formatting-only, readability refactor, TYPO3 best practices alignment, security-focused pass, or full pass.
  Offers /typo3:init when CLAUDE.md is missing.
allowed-tools: Read, Glob, Grep, Bash, Edit
---

# /typo3:code-simplify

Purpose:
- Manually run the TYPO3 Code Simplifier Agent with a user-chosen scope and simplification goals.
- Preserve behavior and produce a detailed report.

## Quick Start

**Default usage (recommended):**
```
/typo3:code-simplify
```
→ Automatically detects changed files and runs a full pass (formatting, refactoring, TYPO3 best practices, security).

**Custom usage:**
```
/typo3:code-simplify goal:format              # Format changed files only
/typo3:code-simplify dir:Classes/Service      # Simplify specific directory
/typo3:code-simplify repo goal:typo3          # Full repository, TYPO3 patterns only
```

## Step 0: CLAUDE.md bootstrap (mandatory)

1) Check if `CLAUDE.md` exists in the repository root.
2) If it exists:
    - Read it fully.
    - Follow its rules.
3) If it does not exist:
    - Ask the user:
      "CLAUDE.md is missing. Should we run /typo3:init first (recommended)?"
    - If yes:
        - Instruct user to run `/typo3:init`.
        - After it exists, read `CLAUDE.md`, then continue.
    - If no:
        - Continue with safe defaults and explicitly report that CLAUDE.md was missing.

## Step 1: Smart defaults for scope and goals

### 1.1 Parse arguments
If the user provided scope or goal arguments in $ARGUMENTS, use them directly.

### 1.2 Auto-detect scope (smart default)
If no scope argument provided:
1. Check for Git changed files:
   - Run: `git diff --name-only && git diff --name-only --staged`
   - Count changed files

2. If changed files exist (> 0):
   - **Use them automatically** (no question needed)
   - Print: "Detected X changed files. Running simplifier on changed files only."

3. If NO changed files exist:
   - Ask: "No changed files detected. Run on which scope? [Directory/Specific Files/Whole Repository]"
   - If Directory: Ask for paths (e.g., `Classes/Service`)
   - If Specific Files: Ask for file paths (one per line)
   - If Whole Repository: Confirm exclusions (vendor/, caches)

### 1.3 Auto-select goals (smart default)
If no goal argument provided:
- **Default to "full pass"** (comprehensive: formatting + refactoring + TYPO3 + security)
- Print: "Using full pass (formatting, refactoring, TYPO3 best practices, security)."
- Add: "Tip: Use 'goal:format' for formatting only, or 'goal:typo3' for TYPO3-specific patterns."

### 1.4 Expert mode (optional customization)
Users can override defaults with arguments:
- Scope: `changed`, `dir:<path>`, `file:<path>`, `repo`
- Goals: `goal:format`, `goal:refactor`, `goal:typo3`, `goal:security`, `goal:full`

If the user explicitly asks to choose interactively, provide the full menu:

**Scope menu (only when explicitly requested):**
"What should I simplify?"
- A) Changed files only (recommended)
- B) A specific directory
- C) Specific file(s)
- D) The whole repository

**Goals menu (only when explicitly requested):**
"What kind of simplification do you want?"
- 1) Formatting and consistency only
- 2) Readability refactors
- 3) TYPO3 best practices alignment
- 4) Security-focused pass
- 5) Full pass (1 + 2 + 3 + 4), conservative edits plus proposals

## Step 3: Execution

- Invoke the agent: `code-simplifier`.
- Provide it:
    - CLAUDE.md status (present or missing)
    - the chosen scope mode
    - the list of files or directories
    - include/exclude filters and file type filters
    - the chosen goals mode
- The agent must print a short scope and goals summary before applying edits.

## Step 4: Output

- Always produce a "TYPO3 Code Simplification Report" with:
    - project context (TYPO3 version, CLAUDE.md status)
    - scope and goals summary
    - applied changes
    - proposals not applied
    - security notes
    - follow-up recommendations

## Arguments

You may pass scope and goals via $ARGUMENTS.

Scope patterns:
- `changed`
  Meaning: changed files only (default)
- `dir:<path>`
  Meaning: simplify everything under the given directory (repeatable)
- `file:<path>`
  Meaning: simplify a single file (repeatable)
- `repo`
  Meaning: simplify the whole repository (with default exclusions)

Goals patterns:
- `goal:format`
  Meaning: formatting and consistency only
- `goal:refactor`
  Meaning: readability refactors only
- `goal:typo3`
  Meaning: TYPO3 best practices alignment (DI, QueryBuilder, Extbase/Fluid correctness)
- `goal:security`
  Meaning: security-focused pass
- `goal:full`
  Meaning: full pass

Examples:
- `/typo3:code-simplify changed goal:full`
- `/typo3:code-simplify dir:Classes/Service goal:typo3`
- `/typo3:code-simplify file:Classes/Controller/FooController.php goal:refactor`
- `/typo3:code-simplify repo goal:security`
