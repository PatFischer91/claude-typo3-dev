---
description: Get TYPO3 Core changelog entries for version upgrades - breaking changes, deprecations, new features, and important information.
allowed-tools: WebSearch, WebFetch
---

# TYPO3 Changelog

Retrieve TYPO3 Core changelog entries to help with version upgrades. Shows breaking changes, deprecations, new features, and important information.

## Usage

```
/typo3:changelog <version> [type]
```

**Arguments:** $ARGUMENTS

Examples:
- `/typo3:changelog 12.4` - All changes in TYPO3 12.4
- `/typo3:changelog 13 Breaking` - Breaking changes in v13
- `/typo3:changelog 12 Deprecation` - Deprecations in v12

**Types:** Breaking, Deprecation, Feature, Important, All (default)

## How to Get Changelog

### Step 1: Search for Changelog Entries

Use WebSearch to find changelog entries:

```
Query: "TYPO3 <version> <type> changes site:docs.typo3.org/c/typo3/cms-core"
```

### Step 2: Provide Curated Summary

For common versions, provide known critical changes:

#### TYPO3 v11 → v12 (Critical Changes)

**Breaking Changes:**
- ObjectManager completely removed - use Dependency Injection
- All controller actions MUST return `ResponseInterface`
- `$GLOBALS['TSFE']` direct access removed - use request attributes
- `switchableControllerActions` removed from plugins
- PHP 8.1+ required

**Deprecations:**
- `GeneralUtility::getUrl()` → use `RequestFactory`
- Old hook system → use PSR-14 Events
- TCA type 'input' with `eval='int'` → use type 'number'
- TCA type 'input' with `renderType='inputDateTime'` → use type 'datetime'

**New Features:**
- New TCA types: number, datetime, email, link, password, color, uuid
- Improved backend UI
- Full PSR-14 event system
- Doctrine DBAL 3.x

#### TYPO3 v12 → v13 (Critical Changes)

**Breaking Changes:**
- PHP 8.2+ required
- Composer-only installation (no classic mode)
- Many deprecated features removed

**New Features:**
- Content Blocks - new way to create content elements
- Site Sets for configuration management
- New backend UI components
- Improved security features

### Step 3: Fetch Detailed Information

If user needs specific details, use WebFetch on:
```
https://docs.typo3.org/c/typo3/cms-core/<major>.4/en-us/Changelog/Index.html
```

### Step 4: Present Results

```markdown
# TYPO3 <version> Changelog

**Type:** <type filter>

## Critical Changes

### Breaking Changes
- <Change 1>
- <Change 2>

### Deprecations
- <Deprecation 1>
- <Deprecation 2>

### New Features
- <Feature 1>
- <Feature 2>

## Useful Links

- **Full Changelog:** https://docs.typo3.org/c/typo3/cms-core/<major>.4/en-us/Changelog/Index.html
- **Upgrade Guide:** https://docs.typo3.org/m/typo3/guide-installation/main/en-us/Upgrade/
- **Breaking Changes:** https://docs.typo3.org/c/typo3/cms-core/<major>.4/en-us/Changelog/Breaking/Index.html
- **Deprecations:** https://docs.typo3.org/c/typo3/cms-core/<major>.4/en-us/Changelog/Deprecation/Index.html

## Migration Tips

<Provide specific migration advice based on the changes>
```

## Quick Reference: Version URLs

| Version | Changelog URL |
|---------|---------------|
| TYPO3 13 | https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog/ |
| TYPO3 12 | https://docs.typo3.org/c/typo3/cms-core/12.4/en-us/Changelog/ |
| TYPO3 11 | https://docs.typo3.org/c/typo3/cms-core/11.5/en-us/Changelog/ |

## Important Notes

- Focus on changes relevant to extension developers
- Highlight security-related changes prominently
- Suggest using TYPO3 Rector for automated migrations
- Always link to official documentation for full details
