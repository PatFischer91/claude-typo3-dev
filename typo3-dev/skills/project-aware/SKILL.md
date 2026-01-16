---
name: project-aware
description: Dynamically adapts suggestions based on the detected TYPO3 version and project configuration. Reads .claude/typo3-project.json for context. Always active when working in TYPO3 projects.
---

# Project-Aware Skill

This skill reads the project configuration from `.claude/typo3-project.json` and adapts all suggestions accordingly.

## Configuration File

The `/typo3:init` command creates `.claude/typo3-project.json` with:
- TYPO3 version
- PHP version
- Project structure
- Installed extensions
- Available tools

## Version-Specific Behavior

### When TYPO3 Version is 11.5

**Allowed but deprecated:**
```php
// Still works but suggest alternatives
$this->objectManager->get(Repository::class);
GeneralUtility::getUrl('https://...');
$GLOBALS['TSFE']->id;
```

**TCA:**
```php
// Old types still valid
'config' => [
    'type' => 'input',
    'eval' => 'int',
]
```

**Controllers:**
- Can return string or void (but suggest ResponseInterface)
- ObjectManager injection still works

### When TYPO3 Version is 12.4

**Required patterns:**
```php
// Must use constructor injection
public function __construct(
    private readonly ProductRepository $productRepository
) {}

// Must return ResponseInterface
public function listAction(): ResponseInterface
{
    return $this->htmlResponse();
}

// Must use Request attributes
$pageId = $this->request->getAttribute('frontend.page.information')->getId();
```

**TCA:**
```php
// Modern types required
'config' => [
    'type' => 'number',
]

'config' => [
    'type' => 'datetime',
    'format' => 'datetime',
]
```

**Forbidden:**
- ObjectManager
- GeneralUtility::getUrl()
- $GLOBALS['TSFE'] direct access
- switchableControllerActions
- or die() (use || die())

### When TYPO3 Version is 13.x

**New features to suggest:**
- Content Blocks for custom content elements
- Site Sets for configuration
- New backend components

**Additional requirements:**
- Composer-only mode
- PHP 8.2+ features

## Project Structure Awareness

### Composer Mode (packages/)
```
Extension path: packages/{extension_key}/
Namespace: {Vendor}\{ExtensionKey}\
```

### Legacy Mode (typo3conf/ext/)
```
Extension path: typo3conf/ext/{extension_key}/
Namespace: {Vendor}\{ExtensionKey}\
```

### DDEV Projects
- Use `ddev exec` for CLI commands
- Database: `ddev describe` for credentials
- URLs: Use DDEV project URL

## Extension Context

When working in an extension directory:
1. Detect extension key from path or composer.json
2. Use correct namespace
3. Follow extension's existing patterns

## Automatic Adjustments

### Code Generation
- Use detected vendor name
- Use correct namespace
- Apply version-specific patterns
- Use project's coding style

### Commands
- Adapt paths to project structure
- Use correct CLI tool (typo3, typo3cms, ddev exec typo3)

### Suggestions
- Only suggest available tools
- Match project's TYPO3 version
- Consider installed extensions

## Reading Project Config

At the start of relevant tasks, check:

```
.claude/typo3-project.json
```

If not found, suggest running `/typo3:init` first.

## Example Adaptations

**User asks:** "Create a Product model"

**For TYPO3 11.5:**
```php
// Can still use @inject (deprecated but works)
// ResponseInterface recommended but not required
public function listAction()
{
    $this->view->assign('products', $this->productRepository->findAll());
}
```

**For TYPO3 12.4:**
```php
// Must use constructor injection
// Must return ResponseInterface
public function listAction(): ResponseInterface
{
    $this->view->assign('products', $this->productRepository->findAll());
    return $this->htmlResponse();
}
```

**For TYPO3 13.x:**
```php
// Suggest Content Blocks if creating content element
// Use latest PHP 8.2+ features
public function listAction(): ResponseInterface
{
    $this->view->assign('products', $this->productRepository->findAll());
    return $this->htmlResponse();
}
```

## Important

- Always check project config before generating code
- If no config found, ask about TYPO3 version or suggest /typo3:init
- Adapt ALL suggestions to the detected version
- Never suggest deprecated patterns for newer versions
- Consider backward compatibility only when explicitly needed
