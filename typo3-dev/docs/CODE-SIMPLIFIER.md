# TYPO3 Code Simplifier Guide

Automatically refactor and clean up TYPO3 code while preserving behavior and following best practices.

## Table of Contents

- [Quick Start](#quick-start)
- [What It Does](#what-it-does)
- [What It Does NOT Do](#what-it-does-not-do)
- [How It Preserves Behavior](#how-it-preserves-behavior)
- [Usage](#usage)
- [Scope Options](#scope-options)
- [Goals Options](#goals-options)
- [Intelligent Hook System](#intelligent-hook-system)
- [Tooling Integration](#tooling-integration)
- [Version Awareness](#version-awareness)
- [Report Format](#report-format)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)

## Quick Start

**Default usage (recommended):**
```
/typo3:code-simplify
```

That's it! The simplifier will:
1. Automatically detect changed files
2. Run a comprehensive pass (formatting, refactoring, TYPO3 best practices, security)
3. Preserve all behavior (outputs, APIs, security patterns)
4. Generate a detailed report

## What It Does

The code simplifier performs safe, behavior-preserving refactoring across multiple dimensions:

### 1. Formatting & Consistency
- PSR-12 code style compliance
- Namespace and import organization
- Whitespace normalization
- Indentation correction (respects .editorconfig)

### 2. Readability Improvements
- Extract complex methods into smaller units
- Reduce nesting depth with early returns
- Rename unclear local variables
- Remove duplicate code

### 3. TYPO3 Best Practices
- **Dependency Injection:** Convert to constructor injection where appropriate
- **QueryBuilder:** Use Doctrine DBAL with named parameters
- **Extbase Controllers:** Ensure slim controllers, move logic to services
- **Fluid Templates:** Remove business logic, use proper escaping
- **FAL:** Use File Abstraction Layer instead of direct file paths
- **Events:** Suggest PSR-14 event patterns (proposals only)

### 4. Security Hardening
- XSS prevention (proper escaping in Fluid)
- SQL injection prevention (QueryBuilder with named parameters)
- CSRF protection awareness
- File upload validation
- Logging sanitization (no passwords/tokens)

### 5. Version-Specific Patterns
- TYPO3 v11/v12/v13 specific refactoring
- Uses correct documentation branch
- Respects deprecations and breaking changes

## What It Does NOT Do

The simplifier is **conservative by design**:

- ❌ Does NOT change functionality or behavior
- ❌ Does NOT modify public APIs (method signatures, service IDs, routes)
- ❌ Does NOT alter database semantics
- ❌ Does NOT weaken security (escaping, validations, permissions)
- ❌ Does NOT automatically migrate hooks to events (proposals only)
- ❌ Does NOT rewrite features or add new functionality

**Uncertain changes become proposals** - you decide whether to apply them.

## How It Preserves Behavior

The simplifier operates under strict safety rules:

### Output Preservation
- Method return values stay identical
- Fluid template output remains the same
- Database query results unchanged
- Error messages consistent

### API Preservation
- Public method signatures intact
- Service registrations unchanged
- Route definitions preserved
- Event listener contracts maintained

### Security Preservation
- Escaping behavior never weakened
- Permission checks remain in place
- Validation logic preserved
- CSRF tokens unchanged

### Semantic Preservation
- Database query semantics identical
- TCA configurations consistent
- Middleware order preserved
- Request/response handling unchanged

### Verification
- Re-reads critical sections after edits
- Syntax validation before finalizing
- Reports "What was NOT changed" section
- Suggests running tests after changes

## Usage

### Default Invocation (Smart Defaults)

```bash
/typo3:code-simplify
```

- Detects changed files automatically
- Runs full pass (all goals)
- Conservative edits + proposals for risky items
- No questions asked if changed files exist

### Custom Scope

```bash
# Specific directory
/typo3:code-simplify dir:Classes/Service

# Specific file
/typo3:code-simplify file:Classes/Controller/ProductController.php

# Whole repository
/typo3:code-simplify repo
```

### Custom Goals

```bash
# Formatting only
/typo3:code-simplify goal:format

# TYPO3 patterns only
/typo3:code-simplify goal:typo3

# Security-focused
/typo3:code-simplify goal:security
```

### Combined

```bash
# Directory with specific goal
/typo3:code-simplify dir:Classes/Domain/Repository goal:typo3

# Whole repo, formatting only
/typo3:code-simplify repo goal:format
```

## Scope Options

### Changed Files (Default)
- Uses Git to detect modified files
- Includes staged and unstaged changes
- Most common and safest option
- **Automatic if changed files exist**

### Directory
- Target specific directory path
- Recursive file discovery
- Respects file type filters
- Example: `Classes/Service`, `Configuration/`

### Specific Files
- Provide exact file paths
- One per line if multiple
- Best for focused refactoring
- Example: `Classes/Controller/FooController.php`

### Whole Repository
- Scans entire codebase
- Excludes `vendor/`, caches, artifacts
- Use for major refactoring initiatives
- Takes longer on large projects

## Goals Options

### 1. Format (Quick)
- PSR-12 formatting
- Import organization
- Whitespace cleanup
- **Fast, non-intrusive**

### 2. Refactor (Readability)
- Extract methods
- Reduce nesting
- Rename variables
- Remove duplication

### 3. TYPO3 (Best Practices)
- DI patterns
- QueryBuilder usage
- Extbase/Fluid correctness
- FAL adoption

### 4. Security (Hardening)
- XSS prevention
- SQL injection fixes
- CSRF awareness
- File handling safety

### 5. Full (Comprehensive - Default)
- All of the above
- Most thorough analysis
- Conservative edits
- Risky items as proposals

## Intelligent Hook System

The plugin includes a smart, context-aware hook that suggests code simplification at the right times **without being annoying**.

### When It Triggers

#### Pre-Commit (Always Active)
- Detects `git commit` commands
- Shows gentle suggestion with file count
- Example: "💡 You're committing 12 files. Consider: /typo3:code-simplify"
- **Non-blocking** - you can commit anyway

#### Session-Based (Intelligent)
- Tracks coding session duration
- Monitors file change activity
- Adapts suggestion strength based on context
- Only triggers after 30+ minutes of active development

### Intelligence Rules

The hook uses smart thresholds to avoid nagging:

| Context | Suggestion Type | Example |
|---------|----------------|---------|
| Recent run (< 15 min) | No prompt | Just ran - don't nag |
| Few changes (< 5 files) | No prompt | Not worth it yet |
| Moderate (10 files, 30 min) | Gentle tip | "💡 Tip: Code simplify available..." |
| Significant (20 files, 45 min) | Clear suggestion | "🔍 Consider running..." |
| Pre-commit | Always suggest | "💡 Before committing..." |

### Smart Cooldown

- Won't suggest again for **15 minutes** after successful run
- Respects your workflow and doesn't interrupt
- Resets session after 60 minutes of inactivity
- Learns from your patterns

### Disable If Needed

If you prefer manual control only:

```bash
# Temporary (current session)
export TYPO3_DISABLE_SIMPLIFY_HOOK=1

# Permanent (edit hooks.json)
# Remove or comment out smart-code-simplify hook
```

Or delete/rename the hook file:
```bash
mv typo3-dev/hooks/smart-code-simplify.sh typo3-dev/hooks/smart-code-simplify.sh.disabled
```

## Tooling Integration

The simplifier automatically detects and respects existing project tooling.

### PHP CS Fixer
**Detected:** `.php-cs-fixer.php`, `.php-cs-fixer.dist.php`

- Reads configuration
- Respects formatting rules
- Focuses on logic improvements instead
- Report notes: "Detected PHP CS Fixer - respecting formatting rules"

### PHPStan
**Detected:** `phpstan.neon`, `phpstan.neon.dist`

- Reads configuration
- Maintains type hint compatibility
- Won't introduce type errors
- Report notes: "Detected PHPStan - maintaining type compatibility"

### Rector
**Detected:** `rector.php`

- Notes which refactors Rector handles
- Avoids duplication
- Report notes: "Detected Rector - some refactors delegated"

### .editorconfig
**Detected:** `.editorconfig` in project root

- Reads indentation settings
- Respects charset and line endings
- Ensures formatting consistency
- Report notes: "Detected .editorconfig - respecting settings"

## Version Awareness

The simplifier is **TYPO3 version-aware** and adapts patterns accordingly.

### Version Detection
1. **CLAUDE.md** (preferred) - explicit version
2. **composer.lock** - installed version
3. **composer.json** - constrained version
4. **User prompt** - if version unknown

### Documentation Branch Resolution
- TYPO3 v11 → uses `11.5` docs
- TYPO3 v12 → uses `12.4` docs
- TYPO3 v13 → uses `13.0` docs

All documentation links in the report use the correct branch.

### Version-Specific Patterns

**TYPO3 v11:**
- Extbase controller actions return ResponseInterface
- QueryBuilder with named parameters
- Constructor DI patterns

**TYPO3 v12:**
- All v11 patterns
- No ObjectManager (removed)
- PSR-14 events preferred
- Content Blocks awareness

**TYPO3 v13:**
- All v12 patterns
- Content Blocks standard
- New TCA column types
- Enhanced site handling

## Report Format

After running, you'll receive a comprehensive report:

```
# TYPO3 Code Simplification Report

## Project Context
- TYPO3 version: 12.4.10
- Version source: composer.lock
- CLAUDE.md: present
- Documentation branch: 12.4
- Detected tooling: PHP CS Fixer, PHPStan
- Scope: changed files (12 files)
- Goals: full pass

## Scope Summary
- Targeted: Classes/Controller/*.php, Classes/Service/*.php
- Filters: PHP files only
- Exclusions: vendor/, var/cache/

## Applied Changes
### ProductController.php (Classes/Controller/ProductController.php:42)
- Extracted listAction query logic to ProductRepository
- Why safe: Query semantics preserved, only location changed
- Docs: https://docs.typo3.org/m/typo3/reference-coreapi/12.4/en-us/...

### ProductService.php (Classes/Service/ProductService.php:87)
- Converted makeInstance to constructor injection
- Why safe: Same service instance, behavior identical
- Docs: https://docs.typo3.org/m/typo3/reference-coreapi/12.4/en-us/...

## What was NOT Changed (Behavior Preserved)
- Public method signatures intact (ProductController API unchanged)
- Escaping behavior unchanged (all Fluid templates still escape by default)
- Database query semantics preserved (same results returned)
- Security validations maintained (price validation still present)
- TCA schemas consistent (no field type changes)

## Proposals (Not Applied)
1. **Migrate SignalSlot to PSR-14 event**
   - File: Classes/Service/ProductService.php:124
   - Why: Requires Services.yaml configuration
   - Confirmation needed: User should verify event listener registration

## Security Notes
- No security issues found
- All Fluid output properly escaped
- QueryBuilder uses named parameters throughout

## Follow-up Recommendations
- Run tests: `composer test`
- Run PHP CS Fixer: `composer fix-cs`
- Run PHPStan: `composer phpstan`
```

## Common Workflows

### Before Committing Changes
```bash
# Make code changes
# ...

# Simplify before commit
/typo3:code-simplify

# Review report and commit
git add .
git commit -m "feat: add product management"
```

### Refactoring Legacy Code
```bash
# Target specific legacy directory
/typo3:code-simplify dir:Classes/Legacy goal:typo3

# Review proposals
# Apply proposals manually if desired

# Run full pass
/typo3:code-simplify dir:Classes/Legacy goal:full
```

### Preparing for Upgrade
```bash
# Security and deprecation check
/typo3:code-simplify repo goal:security

# TYPO3 patterns alignment
/typo3:code-simplify repo goal:typo3

# Review proposals for upgrade-blocking issues
```

### Quick Format Pass
```bash
# Before code review
/typo3:code-simplify goal:format

# Fast, non-intrusive formatting only
```

## Troubleshooting

### No Changed Files Detected
**Issue:** Command says "No changed files detected"

**Solution:**
- Run `git status` to verify changes
- Ensure files are tracked by Git
- Use explicit scope: `/typo3:code-simplify dir:Classes`

### TYPO3 Version Not Detected
**Issue:** Report shows "TYPO3 version: not detected"

**Solution:**
- Run `/typo3:init` to generate CLAUDE.md
- Ensure composer.lock exists
- Manually specify version in CLAUDE.md

### Hook Keeps Suggesting
**Issue:** Hook suggests code-simplify repeatedly

**Solution:**
- This should auto-resolve after running code-simplify (15-min cooldown)
- If persisting, check: `cat .git/.code-simplify-last-run`
- Manually update: `date +%s > .git/.code-simplify-last-run`

### Tool Conflicts with PHP CS Fixer
**Issue:** Both simplifier and PHP CS Fixer changing formatting

**Solution:**
- Simplifier automatically detects PHP CS Fixer
- If conflicts persist, run formatting separately:
  1. `/typo3:code-simplify goal:typo3` (skip formatting)
  2. `composer fix-cs` (run PHP CS Fixer after)

### Proposals Not Actionable
**Issue:** Proposals section has unclear suggestions

**Solution:**
- Proposals are intentionally conservative
- Review each proposal context
- Apply manually if confident
- Skip uncertain proposals

## Examples

### Example 1: Daily Workflow
```bash
# Morning: Start coding session
# ... write code ...

# Before lunch break:
/typo3:code-simplify
# Hook cooldown prevents duplicate suggestions

# Afternoon: Continue coding
# ... more changes ...

# Before end of day:
/typo3:code-simplify
git commit -m "feat: implement user management"
```

### Example 2: Refactoring Sprint
```bash
# Day 1: Controllers
/typo3:code-simplify dir:Classes/Controller goal:full

# Day 2: Services
/typo3:code-simplify dir:Classes/Service goal:full

# Day 3: Repositories
/typo3:code-simplify dir:Classes/Domain/Repository goal:typo3

# Day 4: Full pass
/typo3:code-simplify repo goal:full
```

### Example 3: Pre-Release Cleanup
```bash
# Security audit
/typo3:code-simplify repo goal:security

# Code quality pass
/typo3:code-simplify repo goal:full

# Final format
/typo3:code-simplify repo goal:format

# Run tests
composer test
```

### Example 4: Before/After

**Before (ProductController.php):**
```php
public function listAction() {
    $queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
        ->getQueryBuilderForTable('tx_myext_domain_model_product');
    $products = $queryBuilder
        ->select('*')
        ->from('tx_myext_domain_model_product')
        ->where($queryBuilder->expr()->eq('hidden', 0))
        ->execute()
        ->fetchAll();
    $this->view->assign('products', $products);
}
```

**After running `/typo3:code-simplify`:**
```php
public function listAction(): ResponseInterface
{
    $products = $this->productRepository->findAll();
    $this->view->assign('products', $products);
    return $this->htmlResponse();
}
```

**Changes:**
- ✅ Query moved to repository (proper layer)
- ✅ Added ResponseInterface return type (TYPO3 v11+ requirement)
- ✅ Uses repository pattern (Extbase best practice)
- ✅ Behavior preserved (same products returned)

## Best Practices

### Do
- ✅ Run before committing code
- ✅ Review the report carefully
- ✅ Test after significant refactoring
- ✅ Use smart defaults (`/typo3:code-simplify`)
- ✅ Trust behavior preservation guarantees

### Don't
- ❌ Run on untracked changes without review
- ❌ Ignore proposals - they're valuable insights
- ❌ Skip testing after major refactoring
- ❌ Commit without reviewing applied changes
- ❌ Disable intelligent hook unnecessarily

## Support

### Documentation
- [Plugin README](../../README.md)
- [Installation Guide](./INSTALLATION.md)
- [Configuration Guide](./CONFIGURATION.md)

### Issues
Report issues at: https://github.com/PatFischer91/claude-typo3-dev/issues

### TYPO3 Resources
- [TYPO3 CGL](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/)
- [Extbase Guide](https://docs.typo3.org/m/typo3/guide-extbasefluid/main/en-us/)
- [Security Guidelines](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/)
