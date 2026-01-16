---
description: Assists with TYPO3 version upgrades by scanning for deprecated code, breaking changes, and suggesting migration paths
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# TYPO3 Upgrade Assistant

Scans codebase for deprecated code and assists with major version upgrades.

## Usage

```
/typo3:upgrade [from_version] [to_version]
```

**Parameters:**
- `from_version`: Current TYPO3 version (e.g., `11.5`)
- `to_version`: Target TYPO3 version (e.g., `12.4`)

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Current Setup

- Check `composer.json` for current TYPO3 version
- Identify installed extensions
- Determine PHP version requirements

### 2. Scan for Deprecated Code

Search the entire codebase for deprecated patterns:

#### Removed in TYPO3 v10:
```bash
# $GLOBALS['TYPO3_DB'] - Use Doctrine DBAL
grep -r "\$GLOBALS\['TYPO3_DB'\]" Classes/

# exec_SELECTgetRows, exec_INSERTquery, etc.
grep -r "exec_SELECT\|exec_INSERT\|exec_UPDATE\|exec_DELETE" Classes/
```

#### Removed in TYPO3 v11:
```bash
# switchableControllerActions - Use separate plugins
grep -r "switchableControllerActions" Configuration/

# ObjectManager usage
grep -r "ObjectManager" Classes/

# TYPO3_MODE constant
grep -r "TYPO3_MODE" .
```

#### Removed in TYPO3 v12:
```bash
# GeneralUtility::getUrl() - Use RequestFactory
grep -r "GeneralUtility::getUrl" Classes/

# $GLOBALS['TSFE'] direct access
grep -r "\$GLOBALS\['TSFE'\]" Classes/

# Old hook system - Use PSR-14 Events
grep -r "SC_OPTIONS\|TYPO3_CONF_VARS\['SC_OPTIONS" ext_localconf.php
```

#### Removed in TYPO3 v13:
```bash
# AbstractPlugin (pibase)
grep -r "extends AbstractPlugin\|extends \\\TYPO3\\\CMS\\\Frontend\\\Plugin\\\AbstractPlugin" Classes/

# Non-Composer mode
grep -r "Environment::isComposerMode" Classes/
```

### 3. Check for Breaking Changes

#### PHP Code Issues:

| Pattern | Issue | Solution |
|---------|-------|----------|
| `$GLOBALS['TYPO3_DB']` | Removed in v10 | Use `ConnectionPool` + `QueryBuilder` |
| `GeneralUtility::getUrl()` | Deprecated in v11 | Use `RequestFactory` |
| `$GLOBALS['TSFE']` | Deprecated | Use Request attributes |
| `ObjectManager::get()` | Removed in v12 | Use constructor injection |
| `@inject` annotation | Deprecated | Use `__construct()` injection |
| `or die()` | Non-standard | Use `\|\| die()` |
| `extbase:` FlexForm DS | Changed | Update FlexForm namespace |

#### TCA Issues:

| Pattern | Issue | Solution |
|---------|-------|----------|
| `type => input, eval => int` | Deprecated | Use `type => number` |
| `type => input, renderType => inputDateTime` | Deprecated | Use `type => datetime` |
| `type => text, renderType => t3editor` | Changed | Use `type => text` + `format => ...` |
| `internal_type => db` | Removed | Use `type => group` |

#### TypoScript Issues:

| Pattern | Issue | Solution |
|---------|-------|----------|
| `config.absRefPrefix = auto` | Changed | Now default, remove |
| `CONTENT.select.languageField` | Deprecated | Remove, automatic |
| `filelink` | Removed | Use custom implementation |

### 4. Generate Migration Report

Create a detailed report:

```markdown
# TYPO3 Upgrade Report: v11.5 → v12.4

## Summary
- Files scanned: 45
- Issues found: 12
- Critical: 3
- Warnings: 9

## Critical Issues (Must Fix)

### 1. ObjectManager Usage
**File:** Classes/Controller/ProductController.php:25
**Code:** `$this->objectManager->get(ProductRepository::class)`
**Fix:** Use constructor injection:
```php
public function __construct(
    private readonly ProductRepository $productRepository
) {}
```

### 2. $GLOBALS['TSFE'] Access
**File:** Classes/Service/PageService.php:42
**Code:** `$GLOBALS['TSFE']->id`
**Fix:** Use request attribute:
```php
$pageId = $request->getAttribute('frontend.page.information')->getId();
```

## Warnings (Should Fix)

### 1. GeneralUtility::getUrl()
**File:** Classes/Service/ApiService.php:18
**Fix:** Use RequestFactory

## Recommendations

1. Update PHP to 8.1+ (required for TYPO3 v12)
2. Update composer.json dependencies
3. Run `composer rector` for automated fixes
4. Test thoroughly after changes
```

### 5. Provide Automated Fixes

Offer to automatically fix common issues:

**Fix ObjectManager → Constructor Injection:**
```php
// Before
$repository = $this->objectManager->get(ProductRepository::class);

// After
public function __construct(
    private readonly ProductRepository $productRepository
) {}
// Use: $this->productRepository
```

**Fix $GLOBALS['TSFE'] → Request:**
```php
// Before
$pageId = $GLOBALS['TSFE']->id;
$language = $GLOBALS['TSFE']->sys_language_uid;

// After (in controller/middleware)
$pageInfo = $this->request->getAttribute('frontend.page.information');
$pageId = $pageInfo->getId();

$language = $this->request->getAttribute('language');
$languageId = $language->getLanguageId();
```

**Fix getUrl → RequestFactory:**
```php
// Before
$content = GeneralUtility::getUrl('https://api.example.com/data');

// After
public function __construct(
    private readonly RequestFactory $requestFactory
) {}

$response = $this->requestFactory->request('https://api.example.com/data');
$content = $response->getBody()->getContents();
```

### 6. Update composer.json

Suggest updated dependencies:

```json
{
    "require": {
        "php": "^8.1",
        "typo3/cms-core": "^12.4",
        "typo3/cms-extbase": "^12.4",
        "typo3/cms-fluid": "^12.4"
    }
}
```

### 7. Rector Integration

Suggest Rector rules for automated upgrades:

```bash
# Install TYPO3 Rector
composer require --dev ssch/typo3-rector

# Create rector.php config
# Run Rector
vendor/bin/rector process Classes/
```

## Upgrade Checklist

```markdown
## Pre-Upgrade
- [ ] Backup database and files
- [ ] Check PHP version (8.1+ for v12)
- [ ] Review extension compatibility
- [ ] Read official changelog

## Code Migration
- [ ] Replace $GLOBALS['TYPO3_DB'] with QueryBuilder
- [ ] Replace ObjectManager with DI
- [ ] Replace $GLOBALS['TSFE'] with request attributes
- [ ] Update TCA types (input→number, datetime)
- [ ] Migrate hooks to PSR-14 Events
- [ ] Replace GeneralUtility::getUrl() with RequestFactory

## Post-Upgrade
- [ ] Update composer.json constraints
- [ ] Run: composer update
- [ ] Run: typo3 extension:setup
- [ ] Run: typo3 cache:flush
- [ ] Test all functionality
- [ ] Check deprecation log
```

## Success Message

```
✓ TYPO3 Upgrade Analysis Complete!

Target: TYPO3 11.5 → 12.4

Issues Found:
- Critical: 3 (must fix before upgrade)
- Warnings: 9 (should fix)
- Info: 5 (recommended improvements)

Report saved to: upgrade-report.md

Next steps:
1. Review the upgrade report
2. Fix critical issues first
3. Run Rector for automated fixes
4. Update composer.json
5. Test thoroughly

Resources:
- Changelog: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/12.0/Index.html
- Upgrade Guide: https://docs.typo3.org/m/typo3/guide-installation/main/en-us/Upgrade/
```
