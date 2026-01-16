---
description: Deep analysis of TYPO3 project with detailed configuration. Auto-runs on new projects, use manually for deeper analysis or reconfiguration.
allowed-tools: Read, Glob, Grep, Bash, Write
---

# TYPO3 Project Initialization

Performs a detailed analysis of the TYPO3 project and creates comprehensive configuration.

## Auto-Initialization

**Important:** Basic project detection happens AUTOMATICALLY at session start for TYPO3 projects that haven't been initialized yet (no `CLAUDE.md` in project root). When you run the standard `/init` command, it creates `CLAUDE.md` - after that, auto-detection won't run again. You don't need to run `/typo3:init` manually in most cases.

## When to Use This Command

Run `/typo3:init` manually when you want:
- **Deeper analysis** with site configurations, installed extensions, dev tools
- **Reconfiguration** after major project changes
- **Detailed report** of project structure and recommendations
- **Force refresh** of `.claude/typo3-project.json`

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
5. **Creates `.claude/typo3-project.json`** with all findings
6. **Adjusts Guidelines** to match the detected version

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

### Step 7: Generate Project Configuration

Create `.claude/typo3-project.json`:

```json
{
  "analyzedAt": "2024-01-16T12:00:00Z",
  "typo3": {
    "version": "12.4.10",
    "majorVersion": 12,
    "isLTS": true,
    "composerMode": true
  },
  "php": {
    "version": "8.2",
    "minVersion": "8.1"
  },
  "project": {
    "type": "ddev",
    "rootPath": "/var/www/html",
    "publicPath": "public",
    "configPath": "config"
  },
  "extensions": {
    "local": [
      {
        "key": "my_extension",
        "vendor": "MyVendor",
        "path": "packages/my_extension",
        "version": "1.0.0"
      }
    ],
    "thirdParty": [
      "news",
      "powermail",
      "mask"
    ]
  },
  "sites": [
    {
      "identifier": "main",
      "base": "https://example.com/",
      "languages": ["de", "en"]
    }
  ],
  "tools": {
    "phpCsFixer": true,
    "phpstan": false,
    "rector": false,
    "testingFramework": true
  },
  "guidelines": {
    "useStrictTypes": true,
    "definedGuard": "|| die()",
    "diMethod": "constructor",
    "tcaTypes": "modern",
    "responseInterface": true
  }
}
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

Configuration saved to: .claude/typo3-project.json

I'm now configured for your specific setup.
All my suggestions will match TYPO3 12.4 best practices.

Try these commands:
- /typo3:extension - Create new extension
- /typo3:model - Generate domain model
- /typo3:upgrade - Check for deprecations
```

## Important Notes

- **Auto-init** happens at session start for new projects (no CLAUDE.md yet)
- This command provides **deeper analysis** than auto-init
- The analysis is saved to `.claude/typo3-project.json`
- You can edit the JSON to customize behavior
- Re-run after major project changes (new extensions, TYPO3 upgrade, etc.)
