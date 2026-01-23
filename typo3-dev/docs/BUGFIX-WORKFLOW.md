# TYPO3 Bugfix Workflow Guide

Systematically debug and fix bugs in TYPO3 projects with intelligent automation and flexible control.

## Table of Contents

- [Quick Start](#quick-start)
- [Workflow Modes](#workflow-modes)
- [Step-by-Step Process](#step-by-step-process)
- [TYPO3-Specific Debugging](#typo3-specific-debugging)
- [Chrome MCP Integration](#chrome-mcp-integration)
- [Common Bug Patterns](#common-bug-patterns)
- [Best Practices](#best-practices)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# Interactive (agent suggests mode)
/typo3:bugfix

# With ticket
/typo3:bugfix ticket:T-1234

# With description
/typo3:bugfix "Contact form validation error"

# Specific mode
/typo3:bugfix mode:collaborative
```

**That's it!** The agent will:
1. Understand your bug
2. Suggest appropriate workflow mode
3. Reproduce, analyze, fix, and verify
4. Generate comprehensive report

## Workflow Modes

Choose how much automation you want:

### 🤖 Full Auto
**When to use:**
- Simple bugs (typos, labels, obvious fixes)
- Configuration issues (TypoScript, TCA)
- Trust agent to fix independently

**What happens:**
1. ✅ Reproduces bug automatically
2. ✅ Analyzes root cause
3. ✅ Implements fix
4. ✅ Verifies fix
5. ✅ Reports results

**Your role:** Review final report

**Speed:** ⚡⚡⚡ Fastest (minutes)

---

### 🤝 Collaborative (Recommended)
**When to use:**
- Standard bugs (most cases)
- Want to review before changes
- Balance automation and control

**What happens:**
1. ✅ Reproduces bug automatically
2. ⏸️ **Shows root cause** → you confirm
3. ⏸️ **Proposes fix** → you approve
4. ✅ Applies approved fix
5. ✅ Verifies automatically
6. ✅ Reports results

**Your role:** Review and approve root cause + fix

**Speed:** ⚡⚡ Balanced (10-15 minutes)

---

### 👨‍💻 Assisted
**When to use:**
- Complex bugs (performance, security)
- Critical production issues
- Want full control and understanding
- Learning opportunity

**What happens:**
1. ⏸️ **Shows reproduction steps** → you confirm
2. ⏸️ **Shows analysis** → you review/correct
3. ⏸️ **Suggests fix approach** → you implement
4. ⏸️ **Shows verification** → you verify
5. ✅ Reports results

**Your role:** Guided through each step, you implement

**Speed:** ⚡ Thorough (30+ minutes)

---

## Step-by-Step Process

### Step 1: Bug Understanding

**Agent analyzes:**
- Bug description
- Ticket information (if provided)
- Expected vs actual behavior
- Environment (Frontend/Backend/CLI)
- Affected component

**Example:**
```
Bug Classification:
- Type: Frontend
- Component: tx_myext_contactform
- Complexity: Medium
- Suggested Mode: Collaborative

Reason: Form validation issue requires code changes
and verification, but is straightforward to fix.
```

### Step 2: Mode Selection

**If not specified, agent asks:**
```
How should I handle this bugfix?

1) Full Auto - Fast, fully automated
2) Collaborative - Balanced, you review key steps (Recommended)
3) Assisted - Thorough, maximum control

Choose mode: [1/2/3]
```

**Smart suggestions:**
- Simple bugs → Auto
- Standard bugs → Collaborative
- Complex bugs → Assisted

### Step 3: Bug Reproduction

#### When Reproduction Happens:
✅ Form validation issues
✅ Frontend rendering errors
✅ Backend module bugs
✅ User interaction flows
✅ AJAX/API failures

#### When Reproduction is Skipped:
❌ Label/translation changes
❌ TypoScript configuration
❌ Obvious code typos
❌ TCA adjustments

**Example (Auto/Collaborative):**
```
Reproducing bug via Chrome MCP...

Steps executed:
1. Navigated to /contact
2. Filled form with invalid email
3. Clicked submit
4. Corrected email
5. Clicked submit again

✓ Bug confirmed: Email not sent on second submit

Evidence:
- Screenshot: contact-form-error.png
- Console: No errors
- TYPO3 log: "EmailService not initialized"
```

**Example (Assisted):**
```
Suggested Reproduction Steps:

1. Navigate to /contact
2. Fill form with invalid email (test@invalid)
3. Click submit → validation error appears
4. Correct to valid email (test@example.com)
5. Click submit again
6. Expected: Success message + email sent
7. Actual: No email sent

Can you confirm the bug exists? [y/n]
```

### Step 4: Root Cause Analysis

**Agent investigates:**
- TYPO3 error logs (`var/log/typo3_*.log`)
- Extension code (Controllers, Repositories, Services)
- Configuration (TypoScript, TCA, FlexForms)
- Fluid templates
- Database queries

**Example (Collaborative Mode):**
```
Root Cause Analysis

File: Classes/Controller/ContactController.php:87

Issue:
The EmailService is only called in the initial validation
success branch. When a user corrects errors and re-submits,
the form bypasses email sending due to incorrect session
flash message handling.

Code snippet:
```php
if ($this->request->hasArgument('submitted')) {
    if ($validator->validate($data)) {
        $this->emailService->send($data); // Only here!
    }
}
```

Analysis:
- Flash message persists across requests
- Re-validation logic doesn't trigger email service
- Session state causes bypass

Does this analysis look correct? [y/n]
```

### Step 5: Fix Implementation

**Agent follows TYPO3 best practices:**
- PSR-12 code style
- Constructor injection
- QueryBuilder with named parameters
- Proper type hints
- Security-aware (escaping, validation)

**Example (Collaborative Mode):**
```
Proposed Fix

File: Classes/Controller/ContactController.php

Changes:
- Refactor submitAction() to separate validation and processing
- Ensure emailService->send() called after ANY successful validation
- Clear flash messages on successful submission

Code diff:
```diff
- if ($this->request->hasArgument('submitted')) {
-     if ($validator->validate($data)) {
-         $this->emailService->send($data);
-     }
- }
+ $data = $this->request->getArgument('data');
+ $validationResult = $this->validator->validate($data);
+
+ if ($validationResult->hasErrors()) {
+     $this->addFlashMessage('Please correct errors', '', FlashMessage::ERROR);
+     return $this->redirect('form');
+ }
+
+ $this->emailService->send($data);
+ $this->addFlashMessage('Email sent successfully', '', FlashMessage::OK);
+ return $this->redirect('success');
```

Should I apply this fix? [y/n]
```

**Example (Assisted Mode):**
```
Suggested Fix Approach

File: Classes/Controller/ContactController.php:87

Recommendation:
Refactor submitAction() to ensure email sending occurs
after ANY successful validation, not just initial.

Approach:
1. Extract validation to validateData() method
2. Call emailService->send() after validation passes
3. Clear flash messages on success

Code template provided above.

Please implement this fix manually.
Let me know when done: [done]
```

### Step 6: Fix Verification

**Agent verifies fix works:**
- Repeats reproduction steps via Chrome MCP
- Checks TYPO3 error logs
- Browser console errors
- Regression testing (related features)

**Example (Auto/Collaborative):**
```
Verifying fix via Chrome MCP...

Steps executed:
1. Navigated to /contact
2. Filled form with invalid email
3. Submitted → validation error shown ✓
4. Corrected email
5. Submitted again → success message shown ✓
6. Checked email sent (if testable) ✓

✓ Fix verified successfully

Regression check:
✓ Other forms still work
✓ No new TYPO3 log errors
✓ No console errors
```

### Step 7: Report Generation

**Comprehensive report includes:**
- Bug classification and ticket reference
- Reproduction evidence (screenshots, logs)
- Root cause explanation with code
- Implemented fix with diffs
- Verification results
- Follow-up recommendations
- Changed files list

**Example report:**
```markdown
# TYPO3 Bugfix Report

## Bug Information
- Ticket ID: T-1234
- Description: Contact form doesn't send email after validation error
- Type: Frontend
- Component: tx_myext_contactform
- TYPO3 Version: 12.4.10
- Mode Used: Collaborative

## Reproduction
✓ Successfully reproduced via Chrome MCP

Steps:
1. Navigate to /contact
2. Fill with invalid email
3. Submit (validation error)
4. Correct email
5. Submit again
6. Bug: Email not sent

Evidence:
- Screenshot: form-validation-flow.png
- TYPO3 log: "EmailService not initialized in re-validation"

## Root Cause Analysis
File: Classes/Controller/ContactController.php:87

Issue: EmailService only called in initial validation branch.
Session flash message causes re-validation to bypass email logic.

## Implemented Fix
File: Classes/Controller/ContactController.php

Changes:
- Refactored submitAction() validation flow
- EmailService called after any successful validation
- Flash messages cleared on success

[Code diff included]

## Verification
✓ Fix verified via Chrome MCP
✓ Email sent successfully after error correction
✓ No regressions
✓ No new errors

## Follow-up Recommendations
- [ ] Run tests: composer test
- [ ] Consider adding test: /typo3:test
- [ ] Update documentation if needed
- [ ] Close ticket: T-1234

## Changed Files
- Classes/Controller/ContactController.php (lines 85-105)
```

## TYPO3-Specific Debugging

### Error Logs

**Location:**
```bash
var/log/typo3_*.log
var/log/php_errors.log
```

**Agent reads automatically:**
- Exception traces
- Deprecation warnings
- SQL errors
- Missing class/method errors

### Extension Code Analysis

**Controllers (Extbase):**
```
Classes/Controller/*Controller.php

Common issues:
- Missing ResponseInterface return type
- Wrong action argument types
- Repository not injected
- Redirect without return
```

**Repositories:**
```
Classes/Domain/Repository/*Repository.php

Common issues:
- SQL query errors
- Missing named parameters
- Wrong query constraints
- QueryBuilder misuse
```

**ViewHelpers:**
```
Classes/ViewHelpers/*.php

Common issues:
- Wrong render() signature
- Missing namespace registration
- Incorrect argument types
- Raw output without escaping
```

### Configuration Analysis

**TypoScript:**
```
Configuration/TypoScript/*.typoscript

Common issues:
- Syntax errors (missing braces)
- Wrong condition syntax
- Incorrect plugin paths
- Caching configuration
```

**TCA:**
```
Configuration/TCA/*.php

Common issues:
- Invalid column types
- Missing ctrl fields
- Wrong eval configuration
- Incorrect renderType
```

### Template Analysis

**Fluid:**
```
Resources/Private/Templates/**/*.html

Common issues:
- Unclosed ViewHelper tags
- Missing variable assignments
- f:format.raw misuse (XSS)
- Wrong layout/partial paths
```

## Chrome MCP Integration

### Frontend Testing

**Navigation:**
```
- Navigate to pages
- Fill forms
- Click buttons/links
- Submit data
```

**Inspection:**
```
- Take screenshots
- Capture console errors
- Monitor network requests
- Check DOM structure
```

**Example:**
```
Chrome MCP execution:
1. navigate_page('/contact')
2. fill('input[name="email"]', 'invalid@')
3. click('button[type="submit"]')
4. wait_for('.error-message')
5. take_screenshot('validation-error.png')
6. fill('input[name="email"]', 'valid@example.com')
7. click('button[type="submit"]')
8. wait_for('.success-message')
9. take_screenshot('success.png')
```

### Backend Testing

**Login:**
```
1. Navigate to /typo3
2. Fill credentials
3. Submit login
4. Verify backend access
```

**Module testing:**
```
1. Navigate to module
2. Perform CRUD operations
3. Check flash messages
4. Verify data saved
```

## Common Bug Patterns

### Form Validation Bug
**Symptom:** Form doesn't work after validation error
**Root Cause:** Session state persistence
**Fix:** Clear flash messages, refactor validation logic

### Repository Query Error
**Symptom:** Database exception
**Root Cause:** Missing named parameters or wrong constraints
**Fix:** Use QueryBuilder with createNamedParameter()

### Fluid Rendering Error
**Symptom:** Template not found or variable undefined
**Root Cause:** Wrong variable assignment or path
**Fix:** Verify controller assigns variables, check template paths

### TypoScript Not Applied
**Symptom:** Configuration not working
**Root Cause:** Syntax error or wrong include
**Fix:** Validate syntax, check static template inclusion

### Backend Module 500 Error
**Symptom:** Module crashes
**Root Cause:** Exception in controller or missing dependency
**Fix:** Check logs, inject missing services

## Best Practices

### Before Starting

✅ **Do:**
- Provide clear bug description
- Include ticket reference if available
- Specify expected vs actual behavior
- Mention TYPO3 version if known

❌ **Don't:**
- Skip bug description
- Assume agent knows your setup
- Rush into Auto mode for complex bugs

### During Bugfix

✅ **Do (Collaborative/Assisted):**
- Review root cause analysis carefully
- Ask questions if unclear
- Suggest alternative approaches
- Verify proposed fix makes sense

❌ **Don't:**
- Auto-approve without understanding
- Skip verification step
- Ignore security implications

### After Bugfix

✅ **Do:**
- Run existing tests
- Consider adding new tests
- Update documentation if behavior changed
- Close ticket with reference to fix

❌ **Don't:**
- Skip testing
- Forget to verify fix in production-like environment
- Leave ticket open without update

## Examples

### Example 1: Simple Label Fix

```bash
/typo3:bugfix "Fix typo in contact form submit button" mode:auto
```

**Process:**
1. Agent identifies: Simple label change
2. Skips reproduction (not needed)
3. Finds label in Fluid template
4. Fixes typo
5. Reports completion

**Time:** ~2 minutes

---

### Example 2: Form Validation Bug

```bash
/typo3:bugfix ticket:T-1234 mode:collaborative
```

**Process:**
1. Agent reproduces via Chrome MCP
2. Shows root cause: Session flash issue
3. You confirm analysis ✓
4. Proposes fix with code diff
5. You approve ✓
6. Agent applies and verifies
7. Reports success

**Time:** ~10 minutes

---

### Example 3: Complex Performance Issue

```bash
/typo3:bugfix "Product list slow with 1000+ items" mode:assisted
```

**Process:**
1. Agent suggests profiling steps → you execute
2. Agent shows analysis: N+1 query problem
3. You confirm and provide additional context
4. Agent suggests eager loading approach
5. You implement fix manually
6. Agent provides verification checklist
7. You verify performance improved
8. Agent generates report

**Time:** ~45 minutes

---

## Troubleshooting

### "Bug can't be reproduced"

**Solution:**
- Provide more detailed steps
- Check environment matches description
- Use Assisted mode to guide reproduction
- Verify bug still exists (might be already fixed)

### "Root cause is unclear"

**Solution:**
- Switch to Assisted mode for deeper analysis
- Provide additional context (logs, screenshots)
- Check related components
- Ask agent to analyze specific files

### "Fix doesn't work"

**Solution:**
- Agent detects during verification (won't report success)
- Review root cause analysis again
- Consider alternative approaches
- Use Assisted mode for manual implementation

### "Chrome MCP not available"

**Solution:**
- Agent provides manual verification steps
- Code-based analysis still works
- Skip browser-based reproduction
- Verify manually after fix

### "Want to change mode mid-process"

**Solution:**
- Currently: Restart with different mode
- Future: Mode switching capability

## Integration with Other Features

### Before Bugfix

```bash
# Ensure project configured
/typo3:init

# Check code quality first
/typo3:code-simplify
```

### After Bugfix

```bash
# Add tests
/typo3:test

# Run existing tests
composer test

# Clean up code
/typo3:code-simplify

# Create commit
git commit -m "fix: ..."
```

### Related Commands

- `/typo3:test` - Generate tests for fix
- `/typo3:code-simplify` - Clean up after fix
- `/typo3:test-browser` - Manual browser testing
- `/typo3:docs` - Look up TYPO3 APIs

## Security Considerations

**Agent is security-aware:**
- Never weakens validation
- Maintains proper escaping
- Uses named parameters for queries
- Preserves CSRF protection
- Sanitizes sensitive data in logs

**For security bugs:**
- Agent proposes fixes (no auto-apply)
- Requires user review in all modes
- Documents security implications
- Recommends additional verification

**Example:**
```
Security Fix Proposal

Issue: Potential XSS in product description output

File: Resources/Private/Templates/Product/Show.html

Current (unsafe):
<f:format.raw>{product.description}</f:format.raw>

Proposed (safe):
{product.description}

OR if HTML is intentional:
<f:sanitize.html>{product.description}</f:sanitize.html>

This requires your approval due to security implications.
Approve? [y/n]
```

## Tips & Tricks

**Faster workflow:**
```bash
# Skip reproduction for obvious bugs
/typo3:bugfix skip-reproduction "Fix label typo"

# Always use proposal mode (even in Auto)
/typo3:bugfix fix:proposal mode:auto
```

**Better reports:**
```bash
# Always include ticket for tracking
/typo3:bugfix ticket:T-1234

# Add detailed description
/typo3:bugfix "Product list pagination broken on page 3+"
```

**Learning:**
```bash
# Use Assisted to understand the process
/typo3:bugfix mode:assisted

# Review each step carefully
# Implement fixes manually to learn
```

## Limitations

**Not supported:**
- Architectural changes (requires planning)
- Database migrations (use `/typo3:migration`)
- Breaking API changes (requires user decision)
- Multi-extension bugs (focus one at a time)

**Requires manual intervention:**
- Third-party service integration
- External API issues
- Server configuration problems
- DNS/deployment issues

## Support

### Documentation
- [Plugin README](../../README.md)
- [Installation Guide](./INSTALLATION.md)
- [Chrome DevTools Guide](./CHROME-DEVTOOLS.md)

### TYPO3 Resources
- [Debugging Guide](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Debugging/)
- [Error Handling](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/ErrorAndExceptionHandling/)
- [Testing](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Testing/)
