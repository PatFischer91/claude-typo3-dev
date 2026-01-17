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
2. **Identifies Project Structure** (Composer mode, legacy, DDEV, Docker Compose, etc.)
3. **Analyzes Environment** (Makefile, Docker, Frontend Toolchain)
4. **Finds Extensions** with dependencies and versions
5. **Analyzes Configuration** (Sites, TypoScript, TCA)
6. **Checks Development Tools** (PHP CS Fixer, PHPStan, Rector, Testing Framework)
7. **Reads Git Information** (current branch, recent commits, uncommitted changes)
8. **Analyzes Composer Setup** (custom repositories, patches)
9. **Writes comprehensive project info to `CLAUDE.md`**
10. **Includes TYPO3-specific guidelines** for the detected version

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

# Codeception?
ls -la vendor/bin/codecept

# PHPMD (PHP Mess Detector)?
ls -la vendor/bin/phpmd

# PHP_CodeSniffer?
ls -la vendor/bin/phpcs
```

### Step 7: Detect Makefile & Custom Commands

```bash
# Check for Makefile
ls -la Makefile

# Extract make targets if Makefile exists
grep "^[a-zA-Z0-9_-]*:" Makefile
```

Extract available make commands like:
- `make install`
- `make test`
- `make build`
- `make deploy`
- Custom project commands

### Step 8: Analyze Docker Environment

```bash
# Check for Docker Compose files
ls -la docker-compose.yml
ls -la docker-compose.*.yml
ls -la .project/docker/

# Check for Docker Compose symlinks
ls -la docker-compose.yml | grep "^l"

# Read docker-compose configuration
cat docker-compose.yml
```

Determine:
- Docker Compose setup (unix, mac, windows variants)
- Services configured (web, db, redis, solr, etc.)
- Volume mappings
- Network configuration

### Step 9: Check Frontend Toolchain

```bash
# Check for package.json (Node.js/npm)
ls -la package.json

# Check for frontend build tools
ls -la webpack.config.js
ls -la vite.config.js
ls -la rollup.config.js
ls -la gulpfile.js

# Check for TypeScript
ls -la tsconfig.json

# Check for CSS preprocessors
ls -la tailwind.config.js
ls -la postcss.config.js
```

### Step 10: Analyze Extension Dependencies

For each extension found, read its `composer.json`:

```bash
# For local extension
cat packages/my_extension/composer.json

# Extract dependencies
grep -A 20 '"require"' packages/my_extension/composer.json
```

Extract:
- Extension dependencies
- TYPO3 system extensions used
- Third-party libraries
- Dev dependencies

### Step 11: Read Git Information

```bash
# Current branch
git branch --show-current

# Recent commits
git log --oneline -5

# Check for uncommitted changes
git status --short
```

Extract:
- Current branch name
- Last 5-10 commit messages
- Modified files (if any)
- Untracked files (if any)

### Step 12: Analyze Composer Configuration

```bash
# Read composer.json
cat composer.json
```

Extract:
- Custom repositories (Satis, local packages, VCS)
- Applied patches (via cweagans/composer-patches)
- Custom scripts
- Autoload configuration
- Minimum stability settings

### Step 13: Write Project Configuration to CLAUDE.md

**IMPORTANT**: NEVER replace existing CLAUDE.md content!

**If CLAUDE.md exists:**
1. **Read the entire file first**
2. **Preserve all existing content** (user's custom guidelines, project notes, etc.)
3. **Find the "## TYPO3 Configuration" section** (if it exists)
4. **Update only the TYPO3 section** with new analysis results
5. **Append TYPO3 section** if it doesn't exist yet
6. **Keep everything else untouched**

**If CLAUDE.md doesn't exist:**
1. Create new CLAUDE.md with project name
2. Add TYPO3 Configuration section

**Strategy:**
- Use Read tool to get existing CLAUDE.md content
- Use Edit tool (NOT Write!) to update specific sections
- Only use Write tool if CLAUDE.md doesn't exist yet
- Preserve user's formatting, custom guidelines, and project-specific notes

Example CLAUDE.md content (comprehensive):

```markdown
# Project: [Project Name]

## TYPO3 Configuration

**TYPO3 Version**: 12.4.10 (LTS)
**PHP Version**: 8.2 (required: ^8.1)
**Project Type**: Docker Compose + Composer Mode
**Public Path**: public/
**Config Path**: config/
**Packages Path**: packages/

### Project Structure
- Composer-based TYPO3 installation
- Docker Compose local development environment
- Modern TYPO3 v12 setup
- Web directory: `public/`

### Local Extensions (in packages/)

- **my_shop** (MyVendor/my_shop) - Main shop extension
  - Location: packages/my_shop/
  - Dependencies: georgringer/news, in2code/powermail

- **my_theme** (MyVendor/my_theme) - Frontend theme
  - Location: packages/my_theme/

### Third-Party Extensions

**Content & Forms:**
- powermail (in2code/powermail) ^12.0 - Form builder
- news (georgringer/news) ^11.3 - News management
- mask (mask/mask) ^8.3 - Content elements

**SEO & Analytics:**
- seo (typo3/cms-seo) - Built-in SEO
- google-tag-manager (brotkrueml/google-tag-manager) ^4.0

**Search:**
- solr (apache-solr-for-typo3/solr) ^12.0 - Apache Solr integration

**Development:**
- adminpanel (typo3/cms-adminpanel)
- belog (typo3/cms-belog)

### Sites

- **main** - https://example.com/ (de, en, fr)
  - Website Title: "My TYPO3 Website"
  - Languages: Deutsch (de), English (en), Français (fr)
  - Entry Point: /

- **blog** - https://blog.example.com/ (en)
  - Subdomain site
  - Entry Point: /blog/

### Development Tools

- ✅ **PHP CS Fixer**: vendor/bin/php-cs-fixer
- ✅ **TYPO3 Console**: vendor/bin/typo3 (helhum/typo3-console ^8.0)
- ✅ **TYPO3 Testing Framework**: ^8.0
- ✅ **Codeception**: ^5.1 (with modules: asserts, phpbrowser, webdriver)
- ❌ **PHPStan**: Not installed
- ❌ **Rector**: Not installed

### Makefile Commands

Available make targets:
- `make install` - Install dependencies
- `make test` - Run tests
- `make build` - Build frontend assets
- `make deploy` - Deploy to production
- `make db-import` - Import database

### Docker Environment

- Docker Compose configuration: `.project/docker/docker-compose.unix.yml`
- Symlink: `docker-compose.yml` → `.project/docker/docker-compose.unix.yml`
- Services: web, db, redis, solr

### Frontend Toolchain

- **Node.js**: package.json present
- **Build Tool**: Webpack 5
- **CSS Preprocessor**: PostCSS + Tailwind CSS
- **TypeScript**: tsconfig.json present

### Composer Configuration

**Custom Repositories:**
- Local packages: `./packages/*/`
- Private Satis: https://satis.example.com

**Patches Applied:**
- typo3/cms-backend: "Fix UTF-8 encoding issue in JSON export"

### TYPO3 v12 Guidelines for This Project

Apply these version-specific best practices for TYPO3 12.4:

#### 1. Controllers & Actions
- All controller actions MUST return `Psr\Http\Message\ResponseInterface`
- Use `$this->htmlResponse()`, `$this->jsonResponse()`, or `$this->redirectToUri()`

#### 2. Dependency Injection
- Constructor-based DI only (ObjectManager removed in v12)
- Use `#[Autowire]` attribute when needed
- All dependencies must be injected via constructor

#### 3. TCA Configuration
- Use modern TCA types: `number`, `datetime`, `email`, `color`, `slug`, `category`, `folder`, `file`
- Remove deprecated `eval` options

#### 4. Events & Hooks
- PSR-14 Events only (legacy hooks deprecated)
- Register events in `Configuration/Services.yaml`

#### 5. Request Handling
- Use request attributes instead of `$GLOBALS['TSFE']`
- Access PageArguments via request: `$request->getAttribute('routing')`

#### 6. Database Queries
- QueryBuilder with named parameters only
- Use `createNamedParameter()` for all variables

#### 7. Strict Types & Type Declarations
- Always use `declare(strict_types=1);` at the top of PHP files
- Use proper type hints for all parameters and return types

#### 8. Configuration Files
- Use `defined('TYPO3') || die();` (not `or die()`) in config files

### Git Information

**Current Branch**: develop

**Recent Commits:**
- abc1234: [FEATURE] Add product detail page
- def5678: [BUGFIX] Fix cart calculation
- ghi9012: [TASK] Update TYPO3 to 12.4.10

**Uncommitted Changes:**
- Modified: packages/my_shop/Classes/Controller/ProductController.php
- Untracked: packages/my_shop/Tests/Unit/Domain/Model/ProductTest.php

### Recommendations

#### 1. Install PHPStan for Static Analysis
```bash
composer require --dev phpstan/phpstan saschaegerer/phpstan-typo3
```

Create `phpstan.neon`:
```neon
includes:
    - vendor/saschaegerer/phpstan-typo3/extension.neon

parameters:
    level: 5
    paths:
        - packages/
```

#### 2. Install Rector for Automated Refactoring
```bash
composer require --dev ssch/typo3-rector
```

#### 3. Consider Frontend Optimization
- Add image optimization pipeline
- Implement lazy loading for images
- Configure HTTP/2 server push

### Project-Specific Guidelines

(Include any custom coding standards from existing CLAUDE.md here)

---

## Ready to Help! 🚀

Your TYPO3 12.4 project is well-configured with Docker and modern development tools.

Try these commands:
- `/typo3:extension` - Create new extension
- `/typo3:model` - Generate domain model
- `/typo3:plugin` - Create Extbase plugin
- `/typo3:upgrade` - Check for deprecations
```

### Step 14: Display Analysis Report

```markdown
# 🔍 TYPO3 Project Analysis

## Environment
| Property | Value |
|----------|-------|
| TYPO3 Version | 12.4.10 (LTS) |
| PHP Version | 8.2 |
| Project Type | Docker Compose + Composer |
| Public Path | public/ |
| Config Path | config/ |

## Project Setup
- ✅ Docker Compose (unix variant)
- ✅ Makefile with custom commands
- ✅ Frontend toolchain (Webpack + Tailwind CSS)
- ✅ TypeScript configuration
- ✅ Composer local packages

## Extensions Found
### Local Extensions (3 in packages/)
- **my_shop** (MyVendor/my_shop) v1.0.0
  - Dependencies: georgringer/news, in2code/powermail
- **my_theme** (MyVendor/my_theme) v1.0.0
- **my_api** (MyVendor/my_api) v0.5.0

### Third-Party Extensions (12 installed)
**Content & Forms:**
- powermail (in2code/powermail) ^12.0
- news (georgringer/news) ^11.3

**Search:**
- solr (apache-solr-for-typo3/solr) ^12.0

## Sites
- **main** - https://example.com/ (de, en, fr)
- **blog** - https://blog.example.com/ (en)

## Development Tools
- ✅ PHP CS Fixer available
- ✅ TYPO3 Console (helhum/typo3-console)
- ✅ Codeception with WebDriver
- ❌ PHPStan not installed
- ❌ Rector not installed
- ✅ TYPO3 Testing Framework

## Makefile Commands
Available: install, test, build, deploy, db-import (5 commands)

## Git Status
- **Branch**: develop
- **Recent**: 5 commits analyzed
- **Uncommitted**: 2 modified files, 1 untracked

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

### Step 15: Store Session Context

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

### CLAUDE.md Handling
- **NEVER replace existing CLAUDE.md content** - always read first and only update TYPO3 section
- This command writes TYPO3-specific project info to **CLAUDE.md** (just like `/init`)
- **Preserves all user content**: custom guidelines, project notes, personal preferences
- If CLAUDE.md exists: Update only "## TYPO3 Configuration" section
- If CLAUDE.md doesn't exist: Create new file with TYPO3 section

### Configuration
- All project configuration is stored in CLAUDE.md (no separate JSON files)
- The TYPO3-specific guidelines are loaded automatically at session start
- Re-run after major project changes (new extensions, TYPO3 upgrade, etc.)
- You can edit CLAUDE.md manually to customize behavior

### What Gets Analyzed
- TYPO3 version and project structure
- Local and third-party extensions (with dependencies)
- Development tools (PHP CS Fixer, PHPStan, Rector, etc.)
- Makefile commands
- Docker/DDEV environment
- Frontend toolchain (package.json, webpack, vite, etc.)
- Git status (branch, commits, changes)
- Composer configuration (repositories, patches)
- Site configurations

### When to Re-run
- After TYPO3 version upgrade
- After adding/removing extensions
- After changing project structure (Docker → DDEV)
- After adding new development tools
- When project setup significantly changes
