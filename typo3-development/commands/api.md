---
description: Get TYPO3 Core API reference for specific classes, interfaces, and methods with usage examples.
allowed-tools: WebSearch, WebFetch
---

# TYPO3 API Reference

Get API documentation for TYPO3 Core classes and interfaces with usage examples.

## Usage

```
/typo3:api <class_name> [method_name]
```

**Arguments:** $ARGUMENTS

Examples:
- `/typo3:api ConnectionPool` - Database connection factory
- `/typo3:api RequestFactory` - HTTP requests
- `/typo3:api ActionController htmlResponse` - Controller response method

## How to Get API Reference

### Step 1: Search for Class Documentation

Use WebSearch:

```
Query: "TYPO3 <class_name> API documentation site:docs.typo3.org"
```

Or search GitHub for source code:

```
Query: "TYPO3 <class_name> site:github.com/TYPO3/typo3"
```

### Step 2: Provide Built-in Reference

For common TYPO3 classes, provide the built-in reference below.

### Step 3: Fetch Additional Documentation

Use WebFetch if more details are needed from official documentation.

---

## Built-in API Reference

### TYPO3\CMS\Core\Database\ConnectionPool

**Purpose:** Factory for database connections and QueryBuilder instances.

```php
use TYPO3\CMS\Core\Database\ConnectionPool;

public function __construct(
    private readonly ConnectionPool $connectionPool
) {}

public function findProducts(): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_product');

    return $queryBuilder
        ->select('*')
        ->from('tx_myext_product')
        ->where(
            $queryBuilder->expr()->eq(
                'active',
                $queryBuilder->createNamedParameter(1, \PDO::PARAM_INT)
            )
        )
        ->executeQuery()
        ->fetchAllAssociative();
}
```

**Methods:**
- `getQueryBuilderForTable(string $table): QueryBuilder` - Get QueryBuilder
- `getConnectionForTable(string $table): Connection` - Get raw Connection
- `getConnectionByName(string $name): Connection` - Get Connection by name

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/

---

### TYPO3\CMS\Core\Http\RequestFactory

**Purpose:** Factory for HTTP requests. Replaces deprecated `GeneralUtility::getUrl()`.

```php
use TYPO3\CMS\Core\Http\RequestFactory;
use Psr\Http\Message\ResponseInterface;

public function __construct(
    private readonly RequestFactory $requestFactory
) {}

public function fetchFromApi(string $apiKey): array
{
    $response = $this->requestFactory->request(
        'https://api.example.com/data',
        'GET',
        [
            'headers' => [
                'Authorization' => 'Bearer ' . $apiKey,
                'Accept' => 'application/json',
            ],
            'timeout' => 10,
        ]
    );

    if ($response->getStatusCode() === 200) {
        return json_decode(
            $response->getBody()->getContents(),
            true
        );
    }

    return [];
}
```

**Methods:**
- `request(string $uri, string $method = 'GET', array $options = []): ResponseInterface`

**Options:** `headers`, `timeout`, `query`, `body`, `form_params`, `json`

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Http/

---

### TYPO3\CMS\Extbase\Mvc\Controller\ActionController

**Purpose:** Base class for Extbase plugin controllers.

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Controller;

use Psr\Http\Message\ResponseInterface;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;
use Vendor\MyExtension\Domain\Repository\ProductRepository;

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

    public function showAction(int $product): ResponseInterface
    {
        $product = $this->productRepository->findByUid($product);
        $this->view->assign('product', $product);
        return $this->htmlResponse();
    }
}
```

**Important Methods:**
- `htmlResponse(?string $html = null): ResponseInterface` - Return HTML (required v12+)
- `jsonResponse(?string $json = null): ResponseInterface` - Return JSON
- `redirect(...)` - Redirect to another action
- `forward(...)` - Forward to another action

**Properties:**
- `$this->request` - Current request
- `$this->view` - View instance
- `$this->settings` - Plugin settings from TypoScript

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/Reference/Controller/

---

### TYPO3\CMS\Extbase\Persistence\Repository

**Purpose:** Base class for Extbase repositories handling data persistence.

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Domain\Repository;

use TYPO3\CMS\Extbase\Persistence\Repository;
use TYPO3\CMS\Extbase\Persistence\QueryInterface;

class ProductRepository extends Repository
{
    protected $defaultOrderings = [
        'title' => QueryInterface::ORDER_ASCENDING
    ];

    public function findActive(): array
    {
        $query = $this->createQuery();
        $query->matching(
            $query->equals('active', true)
        );
        return $query->execute()->toArray();
    }

    public function findByCategory(int $categoryUid): array
    {
        $query = $this->createQuery();
        $query->matching(
            $query->contains('categories', $categoryUid)
        );
        return $query->execute()->toArray();
    }
}
```

**Methods:**
- `findAll(): QueryResultInterface` - Get all objects
- `findByUid(int $uid): ?object` - Find by UID
- `add(object $object): void` - Add new object
- `update(object $object): void` - Update object
- `remove(object $object): void` - Remove object
- `createQuery(): QueryInterface` - Create custom query

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/Reference/Domain/Repository/

---

### TYPO3\CMS\Core\Imaging\IconFactory

**Purpose:** Create icons for backend modules and content elements.

```php
use TYPO3\CMS\Core\Imaging\IconFactory;
use TYPO3\CMS\Core\Imaging\Icon;

public function __construct(
    private readonly IconFactory $iconFactory
) {}

public function getIcon(): string
{
    $icon = $this->iconFactory->getIcon(
        'content-text',
        Icon::SIZE_SMALL
    );
    return $icon->render();
}
```

---

### TYPO3\CMS\Core\Resource\ResourceFactory

**Purpose:** Access files and folders via File Abstraction Layer (FAL).

```php
use TYPO3\CMS\Core\Resource\ResourceFactory;

public function __construct(
    private readonly ResourceFactory $resourceFactory
) {}

public function getFile(int $fileUid): ?File
{
    return $this->resourceFactory->getFileObject($fileUid);
}

public function getStorage(int $storageUid): ResourceStorage
{
    return $this->resourceFactory->getStorageObject($storageUid);
}
```

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fal/

---

## Common API Classes Quick Reference

| Class | Purpose |
|-------|---------|
| `ConnectionPool` | Database QueryBuilder factory |
| `RequestFactory` | HTTP requests |
| `ActionController` | Extbase controllers |
| `Repository` | Data persistence |
| `IconFactory` | Backend icons |
| `ResourceFactory` | FAL file access |
| `CacheManager` | Caching |
| `Logger` | Logging |
| `EventDispatcher` | PSR-14 events |
| `SiteConfiguration` | Site settings |

## Important Notes

- Always use Dependency Injection to get class instances
- Never use `GeneralUtility::makeInstance()` for services
- Check TYPO3 version for API availability
- Return `ResponseInterface` from all controller actions (v12+)
