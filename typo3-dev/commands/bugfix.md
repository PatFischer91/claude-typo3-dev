---
description: >
  Systematically fix bugs in TYPO3 projects with intelligent workflow automation.
  Supports bug reproduction, root cause analysis, fix implementation, and verification.
  Choose between Full Auto, Collaborative (default), or Assisted modes for flexible control.
  TYPO3-aware debugging with Chrome MCP integration for frontend/backend testing.
allowed-tools: Read, Glob, Grep, Bash, Edit, mcp__chrome-devtools__*, mcp__plugin_typo3-dev_chrome-devtools__*
---

# /typo3:bugfix

Purpose:
- Systematically debug and fix bugs in TYPO3 projects
- Support multiple workflow modes (Auto/Collaborative/Assisted)
- TYPO3-specific debugging expertise (Extbase, Fluid, TypoScript, TCA)
- Automated reproduction and verification via Chrome MCP
- Generate comprehensive bugfix reports

## Quick Start

**Default usage (interactive mode selection):**
```
/typo3:bugfix
```
→ Agent analyzes bug, suggests appropriate mode, you choose workflow

**With ticket reference:**
```
/typo3:bugfix ticket:T-1234
```

**With bug description:**
```
/typo3:bugfix "Contact form doesn't send email after validation error"
```

**With predefined mode:**
```
/typo3:bugfix mode:auto          # Full automation
/typo3:bugfix mode:collaborative # Collaborative (recommended)
/typo3:bugfix mode:assisted      # Maximum user control
```

**Combined:**
```
/typo3:bugfix ticket:T-1234 mode:collaborative
/typo3:bugfix "Form validation bug" mode:auto
```

## Workflow Modes

### 1. Full Auto
**Best for:** Simple bugs, labels, config issues, obvious fixes

**What happens:**
- ✓ Reproduces bug automatically (Chrome MCP if needed)
- ✓ Analyzes root cause independently
- ✓ Implements fix immediately
- ✓ Verifies fix automatically
- ✓ Generates report

**You do:** Review final report

**Speed:** ⚡⚡⚡ Fastest

### 2. Collaborative (Recommended)
**Best for:** Most bugs, ensures you stay in control

**What happens:**
- ✓ Reproduces bug automatically (Chrome MCP if needed)
- ? Shows root cause analysis → you confirm/correct
- ? Proposes fix with code diff → you approve before applying
- ✓ Verifies fix automatically
- ✓ Generates report

**You do:** Review and approve root cause + fix proposal

**Speed:** ⚡⚡ Balanced

### 3. Assisted
**Best for:** Complex bugs, learning, critical fixes

**What happens:**
- ? Shows reproduction steps → you confirm they work
- ? Shows root cause analysis → you review/correct
- ⚠ Proposes fix approach → you implement manually
- ? Shows verification steps → you verify manually
- ✓ Generates report

**You do:** Confirm each step, implement fix yourself, verify manually

**Speed:** ⚡ Thorough

## Step-by-Step Process

### Step 0: Preparation
1. Check if `CLAUDE.md` exists in project root
2. If missing: Offer to run `/typo3:init` first (recommended)
3. If exists: Read project configuration

### Step 1: Bug Understanding & Mode Selection
1. Parse bug information:
   - Ticket ID (if provided)
   - Bug description
   - Expected vs actual behavior
   - Environment (Frontend/Backend/CLI)
   - Affected component

2. Classify bug and suggest mode:
   - Analyze complexity
   - Determine suggested mode
   - Show recommendation to user

3. Let user choose mode (if not specified in arguments)

### Step 2: Bug Reproduction
Depending on chosen mode:

**Auto/Collaborative:**
- Use Chrome MCP to reproduce bug (if interactive)
- Capture screenshots, console errors, logs
- Document exact steps
- Confirm bug exists

**Assisted:**
- Show suggested reproduction steps
- User confirms bug
- User provides actual steps if different

**Skip reproduction if:**
- Bug is obvious (label change, typo)
- Config/TypoScript only
- User explicitly requests skip
- Assisted mode and user will do manually

### Step 3: Root Cause Analysis

**TYPO3-specific debugging:**
- Read error logs: `var/log/typo3_*.log`
- Analyze extension code (Controllers, Repositories, ViewHelpers, Services)
- Check configuration (TypoScript, TCA, FlexForms, Routing)
- Examine Fluid templates
- Review database queries

**By mode:**
- **Auto:** Analyze independently, proceed to fix
- **Collaborative:** Show findings, wait for confirmation
- **Assisted:** Show detailed analysis, ask for user input/corrections

### Step 4: Fix Implementation

**TYPO3 best practices:**
- Follow PSR-12 and TYPO3 CGL
- Use constructor injection
- QueryBuilder with named parameters
- Return type declarations
- Proper Fluid escaping
- Preserve behavior and APIs

**By mode:**
- **Auto:** Implement immediately
- **Collaborative:** Propose fix with diff, wait for approval
- **Assisted:** Suggest approach, user implements manually

### Step 5: Fix Verification

**Verification methods:**
- Chrome MCP: Repeat reproduction steps, verify bug gone
- Check TYPO3 logs: No new errors
- Regression check: Related functionality still works
- Browser console: No new JavaScript errors

**By mode:**
- **Auto/Collaborative:** Verify automatically
- **Assisted:** Show verification steps, user verifies manually

### Step 6: Report Generation

Generate comprehensive report:
- Bug information
- Reproduction steps (if applicable)
- Root cause analysis
- Implemented fix with code diff
- Verification results
- Follow-up recommendations
- Changed files list

### Step 7: Follow-up (Optional)

Ask user if they want to:
1. Create git commit
2. Run existing tests
3. Generate tests for this fix
4. Update documentation
5. None, done

## Arguments

### Scope Arguments

**Ticket reference:**
```
ticket:T-1234
ticket:#567
```

**Bug description:**
```
"Contact form validation error"
'Backend module throws 500 error'
```

### Mode Arguments

**Predefined modes:**
```
mode:auto          # Full automation
mode:collaborative # Collaborative (recommended, default)
mode:assisted      # Maximum control
```

**Workflow control (advanced):**
```
skip-reproduction  # Skip reproduction step
fix:proposal       # Always propose fixes (don't auto-apply)
verify:manual      # User verifies manually
```

### Examples

**Interactive (choose mode):**
```
/typo3:bugfix
/typo3:bugfix "Form validation issue"
/typo3:bugfix ticket:T-1234
```

**Full auto for simple fix:**
```
/typo3:bugfix "Fix typo in contact form label" mode:auto
/typo3:bugfix ticket:T-567 mode:auto
```

**Collaborative for standard bug:**
```
/typo3:bugfix "Email not sent after validation error" mode:collaborative
/typo3:bugfix ticket:T-1234 mode:collaborative
```

**Assisted for complex issue:**
```
/typo3:bugfix "Performance issue in product list" mode:assisted
/typo3:bugfix ticket:T-999 mode:assisted
```

**Advanced control:**
```
/typo3:bugfix skip-reproduction fix:proposal
/typo3:bugfix mode:auto verify:manual
```

## What Gets Fixed

**Frontend bugs:**
- Form validation issues
- Rendering errors
- JavaScript errors
- AJAX/API failures
- Routing problems

**Backend bugs:**
- Module errors
- TCA configuration issues
- Backend forms
- Flash messages
- Permission issues

**Extension bugs:**
- Extbase controller actions
- Repository queries
- Domain model issues
- ViewHelper errors
- Service logic

**Configuration bugs:**
- TypoScript errors
- TCA issues
- FlexForm problems
- Routing configuration
- Site handling

**Database bugs:**
- Query errors
- SQL injection risks
- Missing named parameters
- Connection issues

## What Doesn't Get Auto-Fixed

**Requires manual decision:**
- Architecture changes
- Database migrations
- API breaking changes
- Security vulnerabilities (proposed only)
- Performance optimizations (suggested only)

**Agent behavior:**
- Conservative approach
- Proposes risky changes
- Preserves public APIs
- Maintains security patterns
- Follows TYPO3 best practices

## Chrome MCP Integration

**Frontend testing:**
- Navigate to pages
- Fill forms
- Click buttons
- Capture screenshots
- Check console errors
- Monitor network requests

**Backend testing:**
- Login to /typo3
- Navigate modules
- Test CRUD operations
- Check flash messages
- Verify data persistence

**Verification:**
- Repeat bug reproduction
- Confirm fix works
- Check for regressions
- Capture evidence

## Output

**Comprehensive report includes:**
- Bug classification
- Reproduction evidence
- Root cause explanation
- Code changes with diffs
- Verification results
- Follow-up recommendations
- Changed files list

**Report is:**
- Customer/ticket ready
- Technical and clear
- Evidence-based
- Actionable

## Best Practices

**Do:**
- ✅ Provide clear bug description
- ✅ Choose appropriate mode
- ✅ Review proposed fixes (Collaborative mode)
- ✅ Verify fixes work
- ✅ Run tests after fix

**Don't:**
- ❌ Skip verification step
- ❌ Use Auto mode for critical bugs
- ❌ Ignore root cause analysis
- ❌ Apply fixes without understanding
- ❌ Skip testing

## Integration with Other Commands

**Before bugfix:**
```
/typo3:init        # Ensure project is configured
```

**After bugfix:**
```
/typo3:test        # Generate tests for the fix
composer test      # Run existing tests
/typo3:code-simplify  # Clean up code if needed
```

## Troubleshooting

**Bug can't be reproduced:**
- Provide more detailed steps
- Check environment (TYPO3 version, extension version)
- Use Assisted mode to guide reproduction

**Root cause unclear:**
- Switch to Assisted mode
- Provide additional context
- Check related components

**Fix doesn't work:**
- Agent will detect during verification
- Re-analyze root cause
- Propose alternative fix

**Chrome MCP not available:**
- Agent will skip browser-based testing
- Manual verification steps provided
- Code-based verification only

## Security Considerations

**Agent follows security best practices:**
- Never weakens validation
- Maintains proper escaping
- Uses QueryBuilder with named parameters
- Preserves CSRF protection
- Sanitizes log output

**Security bugs:**
- Agent proposes fixes (doesn't auto-apply)
- Requires user review
- Documents security implications
- Suggests additional verification

## Notes

- **No automatic test creation:** Agent recommends `/typo3:test` in follow-up
- **TYPO3-aware:** Understands Extbase, Fluid, TypoScript, TCA patterns
- **Version-aware:** Adapts to TYPO3 v11/v12/v13
- **Safe:** Preserves behavior and public APIs
- **Thorough:** Verifies fixes actually work
- **Flexible:** Choose your level of control
