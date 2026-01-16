---
description: Search TYPO3 Extension Repository (TER) for extensions - find packages, check compatibility, get installation instructions.
allowed-tools: WebSearch, WebFetch
---

# TYPO3 Extension Repository Search

Search the TYPO3 Extension Repository (TER) to find extensions, check compatibility, and get installation instructions.

## Usage

```
/typo3:ter <search query> [typo3_version]
```

**Arguments:** $ARGUMENTS

Examples:
- `/typo3:ter news` - Search for news extensions
- `/typo3:ter form builder 12.4` - Form extensions for TYPO3 12.4
- `/typo3:ter powermail` - Get info about powermail extension

## How to Search

### Step 1: Search TER

Use WebSearch to find extensions:

```
Query: "TYPO3 extension <search term> site:extensions.typo3.org"
```

Or search for Composer packages:

```
Query: "TYPO3 <search term> extension composer packagist"
```

### Step 2: Fetch Extension Details

For specific extensions, use WebFetch on:
```
https://extensions.typo3.org/extension/<extension_key>
```

### Step 3: Present Results

```markdown
# TYPO3 Extension Search: <query>

**TYPO3 Version:** <version if specified>

## Found Extensions

### 1. <Extension Name> (<extension_key>)

**Version:** <current version>
**Composer:** `composer require <package-name>`
**Downloads:** <count>
**Compatibility:** TYPO3 <versions>

<Description>

**TER:** https://extensions.typo3.org/extension/<key>
**Repository:** <GitHub/GitLab URL if available>

---

### 2. <Next Extension>
...

## Installation

### Via Composer (Recommended)
```bash
composer require <package-name>
```

### Via Extension Manager
1. Go to Admin Tools > Extensions
2. Search for "<extension_key>"
3. Click "Install"
4. Configure in Settings

## Popular Extensions Quick Reference

| Extension | Composer Package | Description |
|-----------|-----------------|-------------|
| news | georgringer/news | Versatile news system |
| powermail | in2code/powermail | Powerful forms |
| mask | mask/mask | Custom content elements |
| container | b13/container | Container elements |
| solr | apache-solr-for-typo3/solr | Apache Solr integration |
| tt_address | friendsoftypo3/tt-address | Address management |
| form_finisher | Various | Form framework finishers |
```

## Popular Extensions

When users search for common functionality, suggest these proven extensions:

### Forms
- **powermail** (in2code/powermail) - Feature-rich form extension
- **formhandler** (typoheads/formhandler) - Flexible form processing
- **sf_register** (evoweb/sf-register) - User registration

### Content
- **news** (georgringer/news) - News, blogs, events
- **mask** (mask/mask) - Custom content elements without coding
- **content_defender** (ichhabrecht/content-defender) - Content element restrictions
- **container** (b13/container) - Grid/container elements

### SEO & Performance
- **yoast_seo** (yoast-seo-for-typo3/yoast-seo-for-typo3) - Yoast SEO
- **cs_seo** (clickstorm/cs-seo) - SEO features
- **staticfilecache** (lochmueller/staticfilecache) - Static file caching

### Media
- **news** (georgringer/news) - Also handles media
- **fal_gallery** - FAL-based galleries

### E-Commerce
- **cart** (extcode/cart) - Shopping cart system
- **tt_products** - Product catalog

## Important Notes

- Always check TYPO3 version compatibility before installing
- Prefer Composer packages over TER downloads
- Check extension documentation for configuration
- Look at the extension's GitHub/GitLab for issue tracking
- Consider extension maintenance status (last update, stars, downloads)
