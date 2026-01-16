---
name: dependency-injection
description: Promotes constructor-based Dependency Injection over static utility calls and ObjectManager usage. Use when creating classes, controllers, or services.
---

# Dependency Injection Skill

Modern TYPO3 uses constructor-based Dependency Injection (DI). Avoid static calls and deprecated patterns.

## Constructor Injection (Preferred)

### ✅ Modern Approach (TYPO3 v10+)

```php
<?php

declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Vendor\Extension\Domain\Repository\ProductRepository;
use Vendor\Extension\Service\ProductService;
use TYPO3\CMS\Core\Cache\CacheManager;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;
use Psr\Http\Message\ResponseInterface;

class ProductController extends ActionController
{
    public function __construct(
        private readonly ProductRepository $productRepository,
        private readonly ProductService $productService,
        private readonly CacheManager $cacheManager
    ) {}

    public function listAction(): ResponseInterface
    {
        $products = $this->productRepository->findAll();
        $this->view->assign('products', $products);
        return $this->htmlResponse();
    }
}
```

**Key Points:**
- Dependencies injected via `__construct()`
- Use `private readonly` for immutability (PHP 8.1+)
- Auto-wired by TYPO3's dependency injection container
- No manual configuration needed for standard services

### ❌ Deprecated Patterns (Avoid)

```php
// Don't use ObjectManager (removed in v12)
$repository = $this->objectManager->get(ProductRepository::class);

// Avoid GeneralUtility::makeInstance() for services
$service = GeneralUtility::makeInstance(ProductService::class);

// Don't use inject methods
/**
 * @var ProductRepository
 */
protected $productRepository;

public function injectProductRepository(ProductRepository $productRepository): void
{
    $this->productRepository = $productRepository;
}
```

## Service Configuration

### Auto-wiring (Default)

Most services are auto-wired. No configuration needed!

### Manual Configuration (When Needed)

**Configuration/Services.yaml:**

```yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  # Auto-register all classes in Classes/
  Vendor\Extension\:
    resource: '../Classes/*'

  # Exclude certain directories
  Vendor\Extension\Domain\Model\:
    resource: '../Classes/Domain/Model/*'
    autowire: false
    autoconfigure: false

  # Custom service configuration
  Vendor\Extension\Service\ApiClient:
    arguments:
      $apiKey: '%env(API_KEY)%'
      $apiUrl: 'https://api.example.com'

  # Public service (accessible via container)
  Vendor\Extension\Service\PublicService:
    public: true

  # Service with factory
  Vendor\Extension\Service\ComplexService:
    factory: ['@Vendor\Extension\Factory\ServiceFactory', 'create']
```

### Environment Variables

```yaml
services:
  Vendor\Extension\Service\MailService:
    arguments:
      $smtpHost: '%env(SMTP_HOST)%'
      $smtpPort: '%env(int:SMTP_PORT)%'
      $smtpUser: '%env(SMTP_USER)%'
      $smtpPassword: '%env(SMTP_PASSWORD)%'
```

In `.env`:
```
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=user@example.com
SMTP_PASSWORD=secret
```

## Injection Patterns

### Repository Injection

```php
class ProductController extends ActionController
{
    public function __construct(
        private readonly ProductRepository $productRepository
    ) {}
}
```

### Service Injection

```php
class ProductService
{
    public function __construct(
        private readonly ProductRepository $productRepository,
        private readonly CategoryRepository $categoryRepository,
        private readonly EventDispatcherInterface $eventDispatcher
    ) {}
}
```

### TYPO3 Core Services

```php
use TYPO3\CMS\Core\Cache\CacheManager;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\EventDispatcher\EventDispatcher;
use TYPO3\CMS\Core\Mail\MailerInterface;
use Psr\Log\LoggerInterface;

class MyService
{
    public function __construct(
        private readonly CacheManager $cacheManager,
        private readonly ConnectionPool $connectionPool,
        private readonly EventDispatcher $eventDispatcher,
        private readonly MailerInterface $mailer,
        private readonly LoggerInterface $logger
    ) {}
}
```

### PSR Interfaces

```php
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Client\ClientInterface;
use Psr\EventDispatcher\EventDispatcherInterface;
use Psr\Log\LoggerInterface;

class MyController extends ActionController
{
    public function __construct(
        private readonly ClientInterface $httpClient,
        private readonly LoggerInterface $logger
    ) {}
}
```

## When to Use GeneralUtility::makeInstance()

Use `makeInstance()` **only** for:

### 1. Utility Classes (Stateless Helpers)

```php
use TYPO3\CMS\Core\Utility\GeneralUtility;
use TYPO3\CMS\Core\Utility\PathUtility;

$absolutePath = GeneralUtility::getFileAbsFileName('EXT:my_ext/Resources/Public/');
$relativePath = PathUtility::stripPathSitePrefix($absolutePath);
```

### 2. Dynamic Class Instantiation

```php
// When class name is determined at runtime
$className = $settings['handlerClass'];
$handler = GeneralUtility::makeInstance($className);
```

### 3. Value Objects / Data Transfer Objects

```php
// Simple objects without dependencies
$dto = GeneralUtility::makeInstance(ProductDto::class, $title, $price);
```

## Singleton vs Prototype

### Singleton (Default)

One instance shared across all requests:

```yaml
services:
  Vendor\Extension\Service\ConfigurationService:
    shared: true  # Default, can be omitted
```

### Prototype

New instance for each injection:

```yaml
services:
  Vendor\Extension\Service\TemporaryProcessor:
    shared: false  # Create new instance each time
```

## Constructor Arguments

### Type-hinted Arguments (Auto-wired)

```php
public function __construct(
    private readonly ProductRepository $repository,  // Auto-injected
    private readonly LoggerInterface $logger         // Auto-injected
) {}
```

### Scalar Arguments (Must Configure)

```php
public function __construct(
    private readonly ProductRepository $repository,
    private readonly string $apiKey,  // Needs configuration
    private readonly int $timeout = 30
) {}
```

**Configuration:**

```yaml
services:
  Vendor\Extension\Service\ApiService:
    arguments:
      $apiKey: '%env(API_KEY)%'
      $timeout: 60
```

## Factories

For complex object creation:

```php
namespace Vendor\Extension\Factory;

class ApiClientFactory
{
    public function __construct(
        private readonly LoggerInterface $logger
    ) {}

    public function create(string $apiUrl, string $apiKey): ApiClient
    {
        $client = new ApiClient($apiUrl, $apiKey);
        $client->setLogger($this->logger);
        return $client;
    }
}
```

**Service configuration:**

```yaml
services:
  Vendor\Extension\Service\ApiClient:
    factory: ['@Vendor\Extension\Factory\ApiClientFactory', 'create']
    arguments:
      $apiUrl: 'https://api.example.com'
      $apiKey: '%env(API_KEY)%'
```

## Circular Dependencies

### ❌ Problem

```php
class ServiceA
{
    public function __construct(
        private readonly ServiceB $serviceB
    ) {}
}

class ServiceB
{
    public function __construct(
        private readonly ServiceA $serviceA  // Circular!
    ) {}
}
```

### ✅ Solution 1: Lazy Loading

```yaml
services:
  Vendor\Extension\Service\ServiceA:
    lazy: true
```

### ✅ Solution 2: Refactor

Extract shared logic into a third service:

```php
class ServiceA
{
    public function __construct(
        private readonly SharedService $sharedService
    ) {}
}

class ServiceB
{
    public function __construct(
        private readonly SharedService $sharedService
    ) {}
}
```

## Testing with DI

Dependency Injection makes testing easier:

```php
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;

class ProductServiceTest extends UnitTestCase
{
    private ProductService $subject;
    private ProductRepository $repositoryMock;

    protected function setUp(): void
    {
        parent::setUp();

        $this->repositoryMock = $this->createMock(ProductRepository::class);
        $this->subject = new ProductService($this->repositoryMock);
    }

    /**
     * @test
     */
    public function getAvailableProductsReturnsOnlyActiveProducts(): void
    {
        $this->repositoryMock
            ->expects(self::once())
            ->method('findAvailable')
            ->willReturn([/* mock products */]);

        $result = $this->subject->getAvailableProducts();

        self::assertCount(2, $result);
    }
}
```

## Middleware Example

```php
namespace Vendor\Extension\Middleware;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;
use Psr\Log\LoggerInterface;

class AuthenticationMiddleware implements MiddlewareInterface
{
    public function __construct(
        private readonly LoggerInterface $logger
    ) {}

    public function process(
        ServerRequestInterface $request,
        RequestHandlerInterface $handler
    ): ResponseInterface {
        $this->logger->info('Processing request');

        // Authentication logic...

        return $handler->handle($request);
    }
}
```

**Registration in Services.yaml:**

```yaml
services:
  Vendor\Extension\Middleware\AuthenticationMiddleware:
    tags:
      - name: event.listener
        identifier: 'my-ext-auth-middleware'
```

## Common Mistakes

### ❌ Injecting into Models

Domain Models should not have dependencies injected:

```php
// DON'T DO THIS
class Product extends AbstractEntity
{
    public function __construct(
        private readonly ProductRepository $repository  // Wrong!
    ) {}
}
```

Models are data containers, not services!

### ❌ Injecting Request

Don't inject ServerRequestInterface in constructor:

```php
// DON'T DO THIS
class MyController extends ActionController
{
    public function __construct(
        private readonly ServerRequestInterface $request  // Wrong!
    ) {}
}
```

Use `$this->request` in action methods instead.

### ❌ Static Access to DI Services

```php
// DON'T DO THIS
public function myMethod(): void
{
    $service = GeneralUtility::makeInstance(ProductService::class);  // Wrong for services!
    $service->doSomething();
}
```

Inject via constructor instead.

## Best Practices Summary

- ✅ **Constructor injection** - Primary method
- ✅ **`private readonly`** - Immutable dependencies
- ✅ **Auto-wiring** - Let TYPO3 handle it
- ✅ **Services.yaml** - Only when needed
- ✅ **Type hints** - Enable auto-wiring
- ✅ **Interfaces** - Depend on abstractions
- ❌ **ObjectManager** - Removed in v12
- ❌ **Inject methods** - Deprecated pattern
- ❌ **makeInstance for services** - Use DI
- ❌ **Static service access** - Breaks testability

## References

- [Dependency Injection in TYPO3](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/DependencyInjection/)
- [Services.yaml Configuration](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/DependencyInjection/Configuration.html)
- [Symfony DI Component](https://symfony.com/doc/current/service_container.html)
