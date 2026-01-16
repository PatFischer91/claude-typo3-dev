---
description: Search TYPO3 official documentation at docs.typo3.org for APIs, features, configurations, and best practices.
allowed-tools: WebSearch, WebFetch
---

# TYPO3 Documentation Search

Search the official TYPO3 documentation to find information about APIs, features, configurations, and best practices.

## Usage

```
/typo3:docs <search query> [version]
```

**Arguments:** $ARGUMENTS

Examples:
- `/typo3:docs QueryBuilder` - Search for QueryBuilder documentation
- `/typo3:docs Dependency Injection 12.4` - Search DI docs for v12.4
- `/typo3:docs Fluid ViewHelpers` - Search ViewHelper documentation

## How to Search

### Step 1: Perform Web Search

Use WebSearch to find relevant TYPO3 documentation:

```
Query: "TYPO3 <search term> site:docs.typo3.org"
```

If a version is specified, include it:
```
Query: "TYPO3 12.4 <search term> site:docs.typo3.org"
```

### Step 2: Fetch Relevant Pages

If the user needs detailed information, use WebFetch to retrieve the most relevant documentation pages.

### Step 3: Present Results

Format the results clearly:

```markdown
# TYPO3 Documentation: <search term>

## Most Relevant Results

### 1. <Title>
**URL:** <url>
<Brief description or excerpt>

### 2. <Title>
**URL:** <url>
<Brief description or excerpt>

## Quick Reference

<If applicable, provide a quick code example or summary>

## Direct Links

- **Core API Reference:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/
- **TCA Reference:** https://docs.typo3.org/m/typo3/reference-tca/main/en-us/
- **TypoScript Reference:** https://docs.typo3.org/m/typo3/reference-typoscript/main/en-us/
```

## Common Documentation Areas

When searching, consider these documentation sections:

| Topic | URL Pattern |
|-------|-------------|
| Database/QueryBuilder | `/ApiOverview/Database/` |
| Dependency Injection | `/ApiOverview/DependencyInjection/` |
| Fluid Templates | `/ApiOverview/Fluid/` |
| ViewHelpers | `/ApiOverview/Fluid/ViewHelper/` |
| TCA | `/m/typo3/reference-tca/` |
| TypoScript | `/m/typo3/reference-typoscript/` |
| Extbase | `/ExtensionArchitecture/Extbase/` |
| Controllers | `/ExtensionArchitecture/Extbase/Reference/Controller/` |
| Repositories | `/ExtensionArchitecture/Extbase/Reference/Domain/Repository/` |
| Events (PSR-14) | `/ApiOverview/Events/` |
| Middleware | `/ApiOverview/RequestHandling/` |
| Caching | `/ApiOverview/CachingFramework/` |
| Logging | `/ApiOverview/Logging/` |
| FAL | `/ApiOverview/Fal/` |
| Security | `/Security/` |
| Site Configuration | `/ApiOverview/SiteHandling/` |
| Routing | `/ApiOverview/Routing/` |
| CLI Commands | `/ApiOverview/CommandControllers/` |

## Important Notes

- Always include `site:docs.typo3.org` in searches for official documentation
- For version-specific docs, search with the version number (e.g., "TYPO3 12.4")
- The main documentation branch is usually "main" but LTS versions have specific URLs
- Always provide sources with your response
