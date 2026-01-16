---
description: Get TYPO3 Coding Guidelines (CGL) for specific topics - PHP, database, Fluid, security, TypoScript.
allowed-tools: WebSearch, WebFetch
---

# TYPO3 Coding Guidelines

Retrieve TYPO3 Coding Guidelines (CGL) for specific development topics.

## Usage

```
/typo3:cgl [topic]
```

**Arguments:** $ARGUMENTS

**Topics:** php, database, fluid, security, typoscript, all (default)

Examples:
- `/typo3:cgl` - Overview of all guidelines
- `/typo3:cgl php` - PHP coding standards
- `/typo3:cgl database` - Database query guidelines
- `/typo3:cgl security` - Security best practices

## Guidelines Reference

---

### PHP Coding Guidelines

#### File Structure

```php
<?php

declare(strict_types=1);

namespace Vendor\ExtensionKey\Domain\Model;

use TYPO3\CMS\Extbase\DomainObject\AbstractEntity;

class Product extends AbstractEntity
{
    protected string $title = '';
    protected float $price = 0.0;

    public function getTitle(): string
    {
        return $this->title;
    }

    public function setTitle(string $title): void
    {
        $this->title = $title;
    }

    public function getPrice(): float
    {
        return $this->price;
    }
}
```

#### Key Rules

| Rule | Description |
|------|-------------|
| PSR-12 | 4 spaces, braces on new line for classes/methods |
| strict_types | Always `declare(strict_types=1);` |
| Config files | Use `defined('TYPO3') \|\| die();` |
| Line length | Max 120 characters |
| Type hints | Required on all parameters and returns |
| Naming | Classes: StudlyCase, Methods: camelCase |

#### Configuration Files

```php
<?php

defined('TYPO3') || die();

// ext_localconf.php, ext_tables.php, TCA files
```

**Important:** Use `|| die()` NOT `or die()`!

---

### Database Guidelines

#### Always Use QueryBuilder

```php
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Database\Connection;

public function __construct(
    private readonly ConnectionPool $connectionPool
) {}

public function findActiveProducts(int $categoryId): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_product');

    return $queryBuilder
        ->select('uid', 'title', 'price')
        ->from('tx_myext_product')
        ->where(
            $queryBuilder->expr()->eq(
                'category',
                $queryBuilder->createNamedParameter($categoryId, Connection::PARAM_INT)
            ),
            $queryBuilder->expr()->eq(
                'active',
                $queryBuilder->createNamedParameter(1, Connection::PARAM_INT)
            )
        )
        ->orderBy('title', 'ASC')
        ->executeQuery()
        ->fetchAllAssociative();
}
```

#### Key Rules

| Rule | Description |
|------|-------------|
| QueryBuilder | Always use, never raw SQL |
| Named Parameters | Always `createNamedParameter()` |
| Types | Specify `Connection::PARAM_INT`, `PARAM_STR` |
| No concatenation | Never concat user input into SQL |

#### IN() Clause

```php
$queryBuilder->where(
    $queryBuilder->expr()->in(
        'category',
        $queryBuilder->createNamedParameter(
            $categoryIds,
            Connection::PARAM_INT_ARRAY
        )
    )
)
```

---

### Fluid Guidelines

#### Template Structure

```
Resources/Private/
├── Layouts/
│   └── Default.html
├── Templates/
│   └── Product/
│       ├── List.html
│       └── Show.html
└── Partials/
    └── Product/
        └── Item.html
```

#### Template Example

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default" />

<f:section name="main">
    <div class="products">
        <f:for each="{products}" as="product">
            <f:render partial="Product/Item" arguments="{product: product}" />
        </f:for>
    </div>
</f:section>

</html>
```

#### Key Rules

| Rule | Description |
|------|-------------|
| No business logic | Only presentation in templates |
| ViewHelpers | Use for complex presentation logic |
| Data prep | Prepare data in Controller, not template |
| Layouts/Partials | Use for DRY principle |

#### Security

```html
<!-- GOOD: Escaped by default -->
{product.title}

<!-- DANGEROUS: Only for trusted HTML -->
<f:format.raw>{trustedHtml}</f:format.raw>

<!-- GOOD: Proper link handling -->
<f:link.typolink parameter="{product.link}">Read more</f:link.typolink>
```

---

### Security Guidelines

#### Input Validation

```php
// GOOD: Use typed parameters
public function showAction(int $productId): ResponseInterface

// GOOD: Validate input
if ($productId <= 0) {
    throw new \InvalidArgumentException('Invalid product ID');
}
```

#### Database Security

```php
// GOOD: Named parameters
$queryBuilder->expr()->eq(
    'uid',
    $queryBuilder->createNamedParameter($uid, Connection::PARAM_INT)
)

// BAD: String concatenation (SQL Injection!)
$queryBuilder->where("uid = " . $uid)
```

#### Output Security

```html
<!-- GOOD: Escaped by default -->
{userInput}

<!-- BAD: XSS vulnerability -->
<f:format.raw>{userInput}</f:format.raw>
```

#### Key Rules

| Rule | Description |
|------|-------------|
| Validate input | Never trust user input |
| QueryBuilder | Always with named parameters |
| Escape output | Fluid does this by default |
| File uploads | Validate type, size, content |
| No secrets in logs | Never log passwords, tokens |
| CSRF protection | Use backend modules properly |

---

### TypoScript Guidelines

#### File Structure

```
Configuration/
├── TypoScript/
│   ├── constants.typoscript
│   ├── setup.typoscript
│   └── Includes/
│       └── Plugin.typoscript
```

#### Setup Example

```typoscript
plugin.tx_myextension {
    view {
        templateRootPaths.10 = EXT:my_extension/Resources/Private/Templates/
        partialRootPaths.10 = EXT:my_extension/Resources/Private/Partials/
        layoutRootPaths.10 = EXT:my_extension/Resources/Private/Layouts/
    }

    persistence {
        storagePid = {$plugin.tx_myextension.persistence.storagePid}
    }

    settings {
        itemsPerPage = {$plugin.tx_myextension.settings.itemsPerPage}
    }
}
```

#### Key Rules

| Rule | Description |
|------|-------------|
| Constants | Use for configurable values |
| File extension | Use `.typoscript` |
| Includes | Use `@import` not `INCLUDE_TYPOSCRIPT` |
| Paths | Use `EXT:` prefix |

---

## Quick Reference Checklist

Before saving TYPO3 code, verify:

### PHP
- [ ] `declare(strict_types=1);` present
- [ ] `defined('TYPO3') || die();` in config files
- [ ] Proper namespace
- [ ] Type declarations everywhere
- [ ] Constructor DI (no `makeInstance` for services)
- [ ] `ResponseInterface` return in controllers

### Database
- [ ] QueryBuilder used
- [ ] `createNamedParameter()` for all values
- [ ] No string concatenation

### Fluid
- [ ] No business logic
- [ ] No `f:format.raw()` on user input
- [ ] Data prepared in Controller

### Security
- [ ] Input validated
- [ ] No direct `$_GET`, `$_POST` access
- [ ] No `$GLOBALS['TSFE']` usage

## Official Documentation

- **PHP CGL:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/CglPhp/
- **Database:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/
- **Fluid:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fluid/
- **Security:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/
- **TypoScript:** https://docs.typo3.org/m/typo3/reference-typoscript/main/en-us/
