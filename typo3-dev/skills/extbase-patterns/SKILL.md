---
name: extbase-patterns
description: Suggests modern Extbase framework patterns including slim controllers, proper repository usage, and Doctrine DBAL queries. Use when developing Extbase extensions or refactoring legacy code.
---

# Extbase Patterns Skill

When developing TYPO3 Extbase extensions, follow these modern patterns and best practices.

## Slim Controller Pattern

Controllers should be thin and only handle request/response flow. Move business logic to services.

### ❌ Fat Controller (Avoid)

```php
class ProductController extends ActionController
{
    public function listAction(): ResponseInterface
    {
        // Too much logic in controller!
        $products = $this->productRepository->findAll();

        $filtered = [];
        foreach ($products as $product) {
            if ($product->getStock() > 0 && $product->isActive()) {
                $discountedPrice = $product->getPrice() * 0.9;
                $product->setDisplayPrice($discountedPrice);
                $filtered[] = $product;
            }
        }

        usort($filtered, function($a, $b) {
            return $a->getTitle() <=> $b->getTitle();
        });

        $this->view->assign('products', $filtered);
        return $this->htmlResponse();
    }
}
```

### ✅ Slim Controller (Preferred)

```php
class ProductController extends ActionController
{
    public function __construct(
        private readonly ProductRepository $productRepository,
        private readonly ProductService $productService
    ) {}

    public function listAction(): ResponseInterface
    {
        $products = $this->productService->getAvailableProducts();
        $this->view->assign('products', $products);
        return $this->htmlResponse();
    }
}
```

**Service class:**

```php
class ProductService
{
    public function __construct(
        private readonly ProductRepository $productRepository,
        private readonly PricingService $pricingService
    ) {}

    public function getAvailableProducts(): array
    {
        $products = $this->productRepository->findAvailable();

        foreach ($products as $product) {
            $discountedPrice = $this->pricingService->calculateDiscount($product);
            $product->setDisplayPrice($discountedPrice);
        }

        return $products;
    }
}
```

## Repository Patterns

### Constructor Injection

Always use constructor-based dependency injection:

```php
class ProductRepository extends Repository
{
    public function __construct(
        private readonly ConnectionPool $connectionPool
    ) {
        parent::__construct();
    }
}
```

### Custom Queries with QueryBuilder

Use Doctrine DBAL QueryBuilder for complex queries:

```php
public function findAvailable(): array
{
    $query = $this->createQuery();

    return $query->matching(
        $query->logicalAnd(
            $query->greaterThan('stock', 0),
            $query->equals('active', 1)
        )
    )->execute()->toArray();
}
```

For very complex queries, use QueryBuilder directly:

```php
use TYPO3\CMS\Core\Database\ConnectionPool;

public function findByComplexCriteria(array $criteria): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_domain_model_product');

    $queryBuilder
        ->select('*')
        ->from('tx_myext_domain_model_product')
        ->where(
            $queryBuilder->expr()->gt('stock', $queryBuilder->createNamedParameter(0, \PDO::PARAM_INT)),
            $queryBuilder->expr()->eq('active', $queryBuilder->createNamedParameter(1, \PDO::PARAM_INT))
        )
        ->orderBy('title', 'ASC');

    return $queryBuilder->executeQuery()->fetchAllAssociative();
}
```

⚠️ **Important**: Always use named parameters to prevent SQL injection!

### ❌ Deprecated Database Access

```php
// NEVER use these!
$GLOBALS['TYPO3_DB']->exec_SELECTgetRows(...);
$GLOBALS['TYPO3_DB']->exec_INSERTquery(...);
```

### ✅ Modern Database Access

```php
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$queryBuilder = GeneralUtility::makeInstance(ConnectionPool::class)
    ->getQueryBuilderForTable('tx_myext_domain_model_product');
```

Or better: inject ConnectionPool via constructor.

## Dependency Injection

### Modern Constructor Injection (TYPO3 v11+)

```php
class ProductController extends ActionController
{
    public function __construct(
        private readonly ProductRepository $productRepository,
        private readonly ProductService $productService,
        private readonly CacheManager $cacheManager
    ) {}
}
```

Services are auto-wired by default. No manual configuration needed!

### Service Configuration (if needed)

`Configuration/Services.yaml`:

```yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Vendor\Extension\:
    resource: '../Classes/*'

  # Custom service configuration
  Vendor\Extension\Service\ProductService:
    arguments:
      $apiKey: '%env(PRODUCT_API_KEY)%'
```

### ❌ Avoid ObjectManager and makeInstance

```php
// Deprecated in v11, removed in v12
$repository = $this->objectManager->get(ProductRepository::class);

// Avoid for injected dependencies
$service = GeneralUtility::makeInstance(ProductService::class);
```

### ✅ Use Constructor Injection

```php
public function __construct(
    private readonly ProductRepository $productRepository
) {}
```

## Domain Model Patterns

### Rich Domain Models

Add behavior to models, not just getters/setters:

```php
class Product extends AbstractEntity
{
    protected string $title = '';
    protected float $price = 0.0;
    protected int $stock = 0;
    protected bool $active = false;

    // Simple getters/setters...

    // Business logic methods
    public function isAvailable(): bool
    {
        return $this->stock > 0 && $this->active;
    }

    public function calculateDiscountedPrice(float $discountRate): float
    {
        return $this->price * (1 - $discountRate);
    }

    public function reduceStock(int $quantity): void
    {
        if ($quantity > $this->stock) {
            throw new InsufficientStockException(
                'Not enough stock available',
                1234567890
            );
        }

        $this->stock -= $quantity;
    }
}
```

### Value Objects

Use value objects for complex values:

```php
class Money
{
    public function __construct(
        private readonly float $amount,
        private readonly string $currency
    ) {}

    public function getAmount(): float
    {
        return $this->amount;
    }

    public function getCurrency(): string
    {
        return $this->currency;
    }

    public function format(): string
    {
        return number_format($this->amount, 2) . ' ' . $this->currency;
    }
}

// In Product model
protected Money $price;
```

## Avoid $GLOBALS['TSFE']

### ❌ Wrong

```php
public function getCurrentPageId(): int
{
    return $GLOBALS['TSFE']->id;
}
```

### ✅ Correct

Use ServerRequestInterface and TypoScriptFrontendController properly:

```php
use Psr\Http\Message\ServerRequestInterface;
use TYPO3\CMS\Frontend\Controller\TypoScriptFrontendController;

public function myAction(): ResponseInterface
{
    $request = $this->request;
    $currentPage = $request->getAttribute('frontend.page.information');
    $pageId = $currentPage->getId();

    // Or access TSFE through request
    /** @var TypoScriptFrontendController $tsfe */
    $tsfe = $request->getAttribute('frontend.controller');

    // ...
}
```

## Event Dispatching (Modern Hooks)

### ❌ Old Hook System

```php
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processDatamapClass'][]
```

### ✅ PSR-14 Events

**EventListener:**

```php
namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\DataHandling\Event\AfterRecordSavedEvent;

final class AfterProductSavedListener
{
    public function __invoke(AfterRecordSavedEvent $event): void
    {
        if ($event->getTable() === 'tx_myext_domain_model_product') {
            // Handle event
        }
    }
}
```

**Registration in Services.yaml:**

```yaml
services:
  Vendor\Extension\EventListener\AfterProductSavedListener:
    tags:
      - name: event.listener
        identifier: 'my-extension/after-product-saved'
        event: TYPO3\CMS\Core\DataHandling\Event\AfterRecordSavedEvent
```

## Request/Response Handling

All actions must return ResponseInterface:

```php
use Psr\Http\Message\ResponseInterface;

public function listAction(): ResponseInterface
{
    $products = $this->productRepository->findAll();
    $this->view->assign('products', $products);
    return $this->htmlResponse();
}

public function ajaxAction(): ResponseInterface
{
    $data = ['success' => true, 'items' => [...]];
    return $this->jsonResponse(json_encode($data));
}
```

## Validation

Use Extbase validators:

```php
use TYPO3\CMS\Extbase\Validation\Validator\AbstractValidator;

class ProductValidator extends AbstractValidator
{
    protected function isValid(mixed $value): void
    {
        if (!$value instanceof Product) {
            $this->addError('Invalid product', 1234567890);
            return;
        }

        if (empty($value->getTitle())) {
            $this->addError('Title is required', 1234567891);
        }

        if ($value->getPrice() < 0) {
            $this->addError('Price must be positive', 1234567892);
        }
    }
}
```

## Best Practices Summary

- ✅ **Slim controllers** - logic in services
- ✅ **Constructor injection** - no ObjectManager/makeInstance
- ✅ **QueryBuilder** - for complex queries with named parameters
- ✅ **Repository pattern** - all data access in repositories
- ✅ **Rich models** - behavior, not just data containers
- ✅ **PSR-14 events** - not old hook system
- ✅ **ResponseInterface** - return from all actions
- ✅ **Services.yaml** - for service configuration
- ❌ **Avoid $GLOBALS['TSFE']** - use request attributes
- ❌ **Avoid ObjectManager** - deprecated
- ❌ **Avoid $GLOBALS['TYPO3_DB']** - use ConnectionPool

## References

- [Extbase Documentation](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/)
- [Dependency Injection](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/DependencyInjection/)
- [PSR-14 Events](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/)
