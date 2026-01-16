---
name: typo3-coding-standards
description: Enforces TYPO3 Coding Guidelines (CGL) including PSR-12 compliance, proper namespacing, and TYPO3-specific conventions. Use when writing or reviewing PHP code for TYPO3.
---

# TYPO3 Coding Standards Skill

When writing or reviewing TYPO3 PHP code, ensure compliance with TYPO3 Coding Guidelines (CGL):

## PSR-12 Compliance

- Use 4 spaces for indentation (no tabs)
- Opening braces for classes and methods on new line
- Maximum line length of 120 characters
- One class per file
- Proper use of `declare(strict_types=1);`

## TYPO3-Specific Requirements

### File Headers

Every PHP file must start with:

```php
<?php

declare(strict_types=1);

namespace Vendor\ExtensionKey\Domain\Model;

// Class code...
```

### Configuration Files

Configuration files (TCA, ext_localconf.php, ext_tables.php) must include:

```php
<?php

defined('TYPO3') || die();

// Configuration code...
```

⚠️ **Important**: Use `|| die()` NOT `or die()` - this is TYPO3 standard!

## Naming Conventions

### Namespaces

- Format: `Vendor\ExtensionKey\ComponentType\`
- Example: `MyCompany\BlogExtension\Domain\Model\`
- Vendor name in StudlyCase
- Extension key in StudlyCase (even if extension key uses underscores)

### Classes

- StudlyCase: `ProductController`, `UserRepository`
- Suffix with type: `*Controller`, `*Repository`, `*ViewHelper`
- One class per file, filename matches class name

### Methods

- camelCase: `getProducts()`, `initializeAction()`
- Prefix boolean returns with `is`, `has`, `can`: `isValid()`, `hasAccess()`

### Variables

- camelCase: `$productList`, `$currentUser`
- Descriptive names, avoid abbreviations

## Code Organization

### Directory Structure

```
Classes/
├── Controller/       # Controllers
├── Domain/
│   ├── Model/       # Domain Models
│   ├── Repository/  # Repositories
│   └── Validator/   # Custom Validators
├── ViewHelpers/     # Custom ViewHelpers
├── Service/         # Service classes
└── Utility/         # Utility classes (use sparingly)
```

### Business Logic Location

- **Controllers**: Thin, only flow control
- **Models**: Properties and basic validation
- **Repositories**: Data access and queries
- **Services**: Complex business logic
- **ViewHelpers**: Presentation logic only

## Common Violations to Avoid

### ❌ Wrong

```php
<?php
// Missing declare(strict_types=1)
namespace Vendor\Extension\Controller;

class ProductController extends ActionController {  // Brace on same line
    public function listAction() {  // Brace on same line
        $products = $GLOBALS['TYPO3_DB']->exec_SELECTgetRows(...);  // Deprecated
        $this->view->assign('products', $products);
    }
}
```

### ✅ Correct

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Vendor\Extension\Domain\Repository\ProductRepository;
use Psr\Http\Message\ResponseInterface;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;

class ProductController extends ActionController
{
    public function __construct(
        private readonly ProductRepository $productRepository
    ) {}

    public function listAction(): ResponseInterface
    {
        $products = $this->productRepository->findAll();
        $this->view->assign('products', $products);
        return $this->htmlResponse();
    }
}
```

## Type Declarations

- Use type hints for parameters and return types
- Use `declare(strict_types=1);` in every PHP file
- Prefer `readonly` properties (PHP 8.1+)
- Use union types when appropriate: `string|int`
- Use nullable types: `?string` or `string|null`

## Documentation

### DocBlocks

Required for:
- Classes (brief description)
- Public methods (if signature isn't self-explanatory)
- Complex logic

Not required for:
- Getters/setters with obvious purpose
- Methods with self-explanatory signature

Example:

```php
/**
 * Validates product availability based on stock and status
 *
 * @param Product $product The product to validate
 * @return bool True if product is available
 */
public function isAvailable(Product $product): bool
{
    return $product->getStock() > 0 && $product->isActive();
}
```

## Validation Checklist

Before saving TYPO3 PHP code, verify:

- [ ] `declare(strict_types=1);` present
- [ ] `defined('TYPO3') || die();` in config files
- [ ] Proper namespace (Vendor\ExtensionKey\...)
- [ ] Type declarations on parameters and return types
- [ ] PSR-12 compliant (braces, indentation, spacing)
- [ ] No deprecated methods (`$GLOBALS['TYPO3_DB']`, `getUrl()`, etc.)
- [ ] No business logic in controllers
- [ ] Dependency Injection used (not `makeInstance`)
- [ ] No direct `$_GET`, `$_POST`, `$_SESSION` access
- [ ] No `$GLOBALS['TSFE']` usage

## References

- [TYPO3 CGL Official](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/)
- [PSR-12 Specification](https://www.php-fig.org/psr/psr-12/)
- [in2code Claude Instructions](https://github.com/in2code-de/claude-code-instructions/blob/main/CLAUDE.md)
