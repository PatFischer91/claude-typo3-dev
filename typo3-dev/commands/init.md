---
description: Deep analysis of TYPO3 project - detects version, extensions, tools and writes comprehensive config to CLAUDE.md
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# TYPO3 Project Initialization

Performs a detailed analysis of your TYPO3 project and writes all configuration to `CLAUDE.md` (just like the standard `/init` command, but with TYPO3-specific analysis).

## When to Use This Command

Run `/typo3:init` when you want:
- **Detailed TYPO3 analysis** with version detection, extensions, site configs
- **Project initialization** with TYPO3-specific guidelines in CLAUDE.md
- **Reconfiguration** after TYPO3 version upgrades or major changes
- **Update CLAUDE.md** with current project state

## Usage

```
/typo3:init
```

**Arguments:** $ARGUMENTS

## What This Command Does (Deep Analysis)

1. **Detects TYPO3 Version** from composer.json/lock
2. **Identifies Project Structure** (Composer mode, legacy, DDEV, etc.)
3. **Finds Extensions** and their versions
4. **Analyzes Configuration** (Sites, TypoScript, TCA)
5. **Writes comprehensive project info to `CLAUDE.md`**
6. **Includes TYPO3-specific guidelines** for the detected version

## Steps

### Step 1: Detect TYPO3 Version

```bash
# Check composer.json for TYPO3 version
grep -E '"typo3/cms-core"' composer.json

# Check composer.lock for exact version
grep -A2 '"name": "typo3/cms-core"' composer.lock
```

Parse the version and determine:
- Major version (11, 12, 13)
- Minor version (11.5, 12.4, 13.0)
- Is it LTS?

### Step 2: Detect Project Type

Check for:
```bash
# DDEV project?
ls -la .ddev/config.yaml

# Docker Compose?
ls -la docker-compose.yml

# Composer mode?
ls -la vendor/

# Legacy mode? (no vendor)
ls -la typo3conf/ext/

# Helhum typo3-console?
ls -la vendor/helhum/typo3-console

# TYPO3 CMS Base Distribution?
ls -la public/typo3
```

### Step 3: Identify PHP Version

```bash
# From composer.json
grep -E '"php"' composer.json

# Or check running version
php -v
```

### Step 4: Find Extensions

```bash
# Composer-based extensions
grep -E '"typo3-cms-extension"' composer.json

# Local extensions
ls -la packages/
ls -la public/typo3conf/ext/
```

For each extension, extract:
- Extension key
- Vendor name
- Version
- TYPO3 compatibility

### Step 5: Analyze Site Configuration

```bash
# Find site configurations
ls -la config/sites/*/config.yaml

# Check for multi-site setup
find config/sites -name "config.yaml" | wc -l
```

### Step 6: Check Development Tools

```bash
# PHP CS Fixer?
ls -la vendor/bin/php-cs-fixer

# PHPStan?
ls -la vendor/bin/phpstan

# Rector?
ls -la vendor/bin/rector

# TYPO3 Testing Framework?
grep "typo3/testing-framework" composer.json
```

### Step 7: Write Project Configuration to CLAUDE.md

Create or update `CLAUDE.md` in the project root with TYPO3-specific project information.

**If CLAUDE.md exists**: Read it first and append/update the TYPO3 section.
**If CLAUDE.md doesn't exist**: Create it with standard init format + TYPO3 section.

Example CLAUDE.md content:

```markdown
# Project: [Project Name]

## TYPO3 Configuration

**TYPO3 Version**: 12.4.10 (LTS)
**PHP Version**: 8.2 (min: 8.1)
**Project Type**: DDEV + Composer Mode
**Public Path**: public/
**Config Path**: config/

### Project Structure
- Composer-based TYPO3 installation
- DDEV local development environment
- Modern TYPO3 v12 setup

### Local Extensions
- **my_extension** (MyVendor) v1.0.0
  - Location: packages/my_extension/

### Third-Party Extensions
- news (georgringer/news)
- powermail (in2code/powermail)
- mask (mask/mask)

### Sites
- **main**: https://example.com/ (Languages: de, en)

### Development Tools
- ✅ PHP CS Fixer: vendor/bin/php-cs-fixer
- ❌ PHPStan: Not installed
- ❌ Rector: Not installed
- ✅ TYPO3 Testing Framework

### TYPO3 v12 Guidelines for This Project

Apply these version-specific best practices:

1. **Controllers**: All actions MUST return ResponseInterface
2. **Dependency Injection**: Constructor-based DI only (ObjectManager removed)
3. **TCA**: Use modern types (number, datetime, etc.)
4. **Events**: PSR-14 Events only (no legacy hooks)
5. **Request**: Use request attributes instead of $GLOBALS['TSFE']
6. **Database**: QueryBuilder with named parameters only
7. **Strict Types**: Always use `declare(strict_types=1);`
8. **Config Files**: Use `defined('TYPO3') || die();` (not `or die()`)

### Recommendations
- Install PHPStan: `composer require --dev phpstan/phpstan`
- Install Rector: `composer require --dev ssch/typo3-rector`
```

### Step 8: Display Analysis Report

```markdown
# 🔍 TYPO3 Project Analysis

## Environment
| Property | Value |
|----------|-------|
| TYPO3 Version | 12.4.10 (LTS) |
| PHP Version | 8.2 |
| Project Type | DDEV + Composer |
| Public Path | public/ |

## Extensions Found
### Local Extensions (in packages/)
- **my_extension** (MyVendor) v1.0.0

### Third-Party Extensions
- news (georgringer/news)
- powermail (in2code/powermail)
- mask (mask/mask)

## Sites
- **main** - https://example.com/ (de, en)

## Development Tools
- ✅ PHP CS Fixer available
- ❌ PHPStan not installed
- ❌ Rector not installed
- ✅ TYPO3 Testing Framework

## Version-Specific Guidelines Applied

For TYPO3 12.4:
- ✅ Use `ResponseInterface` for all controller actions
- ✅ Constructor-based Dependency Injection (no ObjectManager)
- ✅ Modern TCA types (number, datetime, etc.)
- ✅ PSR-14 Events (no legacy hooks)
- ✅ Request attributes instead of $GLOBALS['TSFE']
- ✅ QueryBuilder with named parameters

## Recommendations

1. **Install PHPStan** for static analysis:
   ```bash
   composer require --dev phpstan/phpstan
   ```

2. **Install Rector** for automated upgrades:
   ```bash
   composer require --dev ssch/typo3-rector
   ```

## Session Configuration

I've configured this session for TYPO3 12.4 development.
All my suggestions will follow v12 best practices.

Ready to help with your TYPO3 project! 🚀
```

### Step 9: Store Session Context

The analysis is stored and will be used throughout the session:
- Commands adapt to detected version
- Code suggestions match project structure
- Extension scaffolding uses correct paths
- TCA types match TYPO3 version

## Version-Specific Adjustments

### TYPO3 v11
- ObjectManager still available (deprecated)
- Some old TCA types still work
- switchableControllerActions still available
- $GLOBALS['TSFE'] accessible

### TYPO3 v12
- ObjectManager removed
- Modern TCA types required
- ResponseInterface required
- Strict DI enforcement
- PSR-14 Events only

### TYPO3 v13
- Content Blocks available
- New backend UI
- Composer-only mode
- Site Sets feature

## Success Message

```
✓ TYPO3 Project initialized!

Project: TYPO3 12.4.10 (Composer/DDEV)
Extensions: 1 local, 3 third-party
Sites: 1 configured

Configuration written to: CLAUDE.md

I'm now configured for your specific setup.
All my suggestions will match TYPO3 12.4 best practices.

Try these commands:
- /typo3:extension - Create new extension
- /typo3:model - Generate domain model
- /typo3:upgrade - Check for deprecations
```

## Important Notes

- This command writes TYPO3-specific project info to **CLAUDE.md** (just like `/init`)
- All project configuration is stored in CLAUDE.md (no separate JSON files)
- The TYPO3-specific guidelines are loaded automatically at session start
- Re-run after major project changes (new extensions, TYPO3 upgrade, etc.)
- You can edit CLAUDE.md manually to customize behavior
