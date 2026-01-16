---
name: typo3-api
description: Provides knowledge of TYPO3 Core APIs, their proper usage, and common patterns. Use when working with TYPO3 Core functionality like caching, logging, or file handling.
---

# TYPO3 API Skill

TYPO3 provides comprehensive Core APIs. Use these instead of custom implementations or deprecated methods.

## HTTP Requests - RequestFactory

### ❌ Deprecated Methods

```php
// Don't use these!
$content = GeneralUtility::getUrl('https://api.example.com/data');  // Deprecated
$ch = curl_init();  // Don't use raw cURL
```

### ✅ Use RequestFactory

```php
use TYPO3\CMS\Core\Http\RequestFactory;
use Psr\Http\Client\ClientExceptionInterface;

public function __construct(
    private readonly RequestFactory $requestFactory,
    private readonly LoggerInterface $logger
) {}

public function fetchFromApi(): array
{
    try {
        $response = $this->requestFactory->request(
            'https://api.example.com/products',
            'GET',
            [
                'headers' => [
                    'Authorization' => 'Bearer ' . $this->apiToken,
                    'Accept' => 'application/json',
                    'User-Agent' => 'TYPO3-Extension/1.0'
                ],
                'timeout' => 10,
                'verify' => true,  // Verify SSL certificate
            ]
        );

        if ($response->getStatusCode() !== 200) {
            throw new \RuntimeException('API request failed with status ' . $response->getStatusCode());
        }

        return json_decode($response->getBody()->getContents(), true);

    } catch (ClientExceptionInterface $e) {
        $this->logger->error('API request failed', [
            'exception' => $e->getMessage()
        ]);
        return [];
    }
}
```

### POST Request

```php
$response = $this->requestFactory->request(
    'https://api.example.com/products',
    'POST',
    [
        'headers' => [
            'Content-Type' => 'application/json',
        ],
        'json' => [
            'title' => 'New Product',
            'price' => 99.99
        ]
    ]
);
```

## Caching API

### Cache Manager

```php
use TYPO3\CMS\Core\Cache\CacheManager;
use TYPO3\CMS\Core\Cache\Frontend\FrontendInterface;

public function __construct(
    private readonly CacheManager $cacheManager
) {}

public function getProducts(): array
{
    $cache = $this->cacheManager->getCache('myext_products');
    $cacheIdentifier = 'product_list_' . $this->currentPageId;

    // Try to get from cache
    $products = $cache->get($cacheIdentifier);

    if ($products === false) {
        // Cache miss - fetch from database
        $products = $this->productRepository->findAll();

        // Store in cache (lifetime: 3600 seconds)
        $cache->set(
            $cacheIdentifier,
            $products,
            ['products', 'page_' . $this->currentPageId],  // Tags
            3600  // Lifetime in seconds
        );
    }

    return $products;
}
```

### Register Custom Cache

**ext_localconf.php:**

```php
if (!isset($GLOBALS['TYPO3_CONF_VARS']['SYS']['caching']['cacheConfigurations']['myext_products'])) {
    $GLOBALS['TYPO3_CONF_VARS']['SYS']['caching']['cacheConfigurations']['myext_products'] = [
        'frontend' => \TYPO3\CMS\Core\Cache\Frontend\VariableFrontend::class,
        'backend' => \TYPO3\CMS\Core\Cache\Backend\Typo3DatabaseBackend::class,
        'options' => [
            'defaultLifetime' => 3600,
        ],
    ];
}
```

### Flush Cache by Tag

```php
$cache = $this->cacheManager->getCache('myext_products');

// Flush all entries with tag 'products'
$cache->flushByTag('products');

// Flush all entries with tag 'page_123'
$cache->flushByTag('page_123');
```

### Cache Backends

- **Typo3DatabaseBackend** - Store in database
- **FileBackend** - Store in files
- **RedisBackend** - Store in Redis (requires PHP Redis extension)
- **ApcuBackend** - Store in APCu (fast, but not shared across processes)

## Logging API

### PSR-3 Logger

```php
use Psr\Log\LoggerInterface;

public function __construct(
    private readonly LoggerInterface $logger
) {}

public function processOrder(Order $order): void
{
    $this->logger->info('Processing order', [
        'orderId' => $order->getUid(),
        'customer' => $order->getCustomer()->getName(),
    ]);

    try {
        $this->orderService->process($order);
        $this->logger->notice('Order processed successfully', ['orderId' => $order->getUid()]);
    } catch (\Exception $e) {
        $this->logger->error('Order processing failed', [
            'orderId' => $order->getUid(),
            'exception' => $e->getMessage(),
            'trace' => $e->getTraceAsString(),
        ]);
        throw $e;
    }
}
```

### Log Levels

```php
$this->logger->emergency('System is down');  // 0 - System unusable
$this->logger->alert('Action must be taken immediately');  // 1
$this->logger->critical('Critical conditions');  // 2
$this->logger->error('Error conditions');  // 3
$this->logger->warning('Warning conditions');  // 4
$this->logger->notice('Normal but significant');  // 5
$this->logger->info('Informational messages');  // 6
$this->logger->debug('Debug-level messages');  // 7
```

### Configure Logger

**ext_localconf.php:**

```php
$GLOBALS['TYPO3_CONF_VARS']['LOG']['Vendor']['MyExtension']['writerConfiguration'] = [
    \TYPO3\CMS\Core\Log\LogLevel::ERROR => [
        \TYPO3\CMS\Core\Log\Writer\FileWriter::class => [
            'logFileInfix' => 'myextension_errors',
        ],
    ],
];
```

## File Abstraction Layer (FAL)

### Get File from FAL

```php
use TYPO3\CMS\Core\Resource\ResourceFactory;

public function __construct(
    private readonly ResourceFactory $resourceFactory
) {}

public function getFile(int $fileUid): ?\TYPO3\CMS\Core\Resource\File
{
    try {
        return $this->resourceFactory->getFileObject($fileUid);
    } catch (\Exception $e) {
        $this->logger->error('File not found', ['fileUid' => $fileUid]);
        return null;
    }
}
```

### Upload File

```php
$storage = $this->resourceFactory->getDefaultStorage();
$folder = $storage->getFolder('user_uploads/');

$uploadedFile = $storage->addUploadedFile(
    [
        'tmp_name' => $tempPath,
        'name' => $filename,
        'size' => $filesize,
    ],
    $folder,
    $filename,
    \TYPO3\CMS\Core\Resource\DuplicationBehavior::RENAME
);
```

### Process Images

```php
use TYPO3\CMS\Core\Imaging\ImageManipulation\CropVariantCollection;
use TYPO3\CMS\Core\Resource\FileReference;

public function getProcessedImage(FileReference $fileReference, int $width): string
{
    $processingInstructions = [
        'width' => $width . 'c',
        'height' => (int)($width / 1.5) . 'c',  // 3:2 ratio
        'crop' => $fileReference->getProperty('crop'),
    ];

    $processedImage = $fileReference->getOriginalFile()->process(
        \TYPO3\CMS\Core\Resource\ProcessedFile::CONTEXT_IMAGECROPSCALEMASK,
        $processingInstructions
    );

    return $processedImage->getPublicUrl();
}
```

## Context API

### Get Current Context

```php
use TYPO3\CMS\Core\Context\Context;

public function __construct(
    private readonly Context $context
) {}

public function getCurrentInfo(): array
{
    // Language
    $languageAspect = $this->context->getAspect('language');
    $languageId = $languageAspect->getId();

    // Frontend User
    $userAspect = $this->context->getAspect('frontend.user');
    $isLoggedIn = $userAspect->isLoggedIn();
    $userId = $userAspect->get('id');

    // Date/Time
    $dateTimeAspect = $this->context->getAspect('date');
    $timestamp = $dateTimeAspect->get('timestamp');

    // Workspace
    $workspaceAspect = $this->context->getAspect('workspace');
    $workspaceId = $workspaceAspect->getId();
    $isLive = $workspaceAspect->isLive();

    // Visibility
    $visibilityAspect = $this->context->getAspect('visibility');
    $showHidden = $visibilityAspect->includeHiddenContent();

    return compact('languageId', 'isLoggedIn', 'userId', 'timestamp', 'workspaceId');
}
```

## PSR-14 Events

### Dispatching Events

```php
use Psr\EventDispatcher\EventDispatcherInterface;
use Vendor\MyExtension\Event\ProductCreatedEvent;

public function __construct(
    private readonly EventDispatcherInterface $eventDispatcher
) {}

public function createProduct(array $data): Product
{
    $product = new Product();
    // ... set properties

    $this->productRepository->add($product);

    // Dispatch event
    $event = new ProductCreatedEvent($product, $data);
    $this->eventDispatcher->dispatch($event);

    return $product;
}
```

### Creating Custom Event

```php
<?php

declare(strict_types=1);

namespace Vendor\MyExtension\Event;

final class ProductCreatedEvent
{
    public function __construct(
        private Product $product,
        private array $data
    ) {}

    public function getProduct(): Product
    {
        return $this->product;
    }

    public function getData(): array
    {
        return $this->data;
    }
}
```

### Event Listener

```php
namespace Vendor\MyExtension\EventListener;

use Vendor\MyExtension\Event\ProductCreatedEvent;

final class SendProductNotificationListener
{
    public function __construct(
        private readonly MailerInterface $mailer,
        private readonly LoggerInterface $logger
    ) {}

    public function __invoke(ProductCreatedEvent $event): void
    {
        $product = $event->getProduct();

        $this->logger->info('Product created', [
            'productId' => $product->getUid(),
            'title' => $product->getTitle(),
        ]);

        // Send notification email...
    }
}
```

**Register in Services.yaml:**

```yaml
services:
  Vendor\MyExtension\EventListener\SendProductNotificationListener:
    tags:
      - name: event.listener
        identifier: 'myext-product-created-notification'
        event: Vendor\MyExtension\Event\ProductCreatedEvent
```

## Site Configuration

### Get Site Configuration

```php
use TYPO3\CMS\Core\Site\SiteFinder;

public function __construct(
    private readonly SiteFinder $siteFinder
) {}

public function getCurrentSiteInfo(): array
{
    $site = $this->request->getAttribute('site');

    $baseUrl = $site->getBase()->__toString();
    $languages = $site->getLanguages();
    $rootPageId = $site->getRootPageId();

    $settings = $site->getConfiguration();
    $customSetting = $settings['myCustomSetting'] ?? null;

    return compact('baseUrl', 'languages', 'rootPageId', 'customSetting');
}
```

## FlashMessages

### Add Flash Messages

```php
use TYPO3\CMS\Core\Messaging\AbstractMessage;
use TYPO3\CMS\Core\Messaging\FlashMessage;
use TYPO3\CMS\Core\Messaging\FlashMessageService;

public function __construct(
    private readonly FlashMessageService $flashMessageService
) {}

public function showMessages(): void
{
    $messageQueue = $this->flashMessageService->getMessageQueueByIdentifier();

    // Info message
    $message = GeneralUtility::makeInstance(
        FlashMessage::class,
        'Product saved successfully',
        'Success',
        AbstractMessage::OK,
        true  // Store in session
    );
    $messageQueue->enqueue($message);

    // Error message
    $message = GeneralUtility::makeInstance(
        FlashMessage::class,
        'Failed to save product',
        'Error',
        AbstractMessage::ERROR
    );
    $messageQueue->enqueue($message);
}
```

### In Extbase Controller

```php
$this->addFlashMessage(
    'Product saved successfully',
    'Success',
    AbstractMessage::OK,
    true
);
```

## Email API

### Send Email

```php
use Symfony\Component\Mime\Address;
use TYPO3\CMS\Core\Mail\FluidEmail;
use TYPO3\CMS\Core\Mail\MailerInterface;

public function __construct(
    private readonly MailerInterface $mailer
) {}

public function sendOrderConfirmation(Order $order): void
{
    $email = GeneralUtility::makeInstance(FluidEmail::class);

    $email
        ->to(new Address($order->getCustomer()->getEmail(), $order->getCustomer()->getName()))
        ->from(new Address('shop@example.com', 'My Shop'))
        ->subject('Order Confirmation #' . $order->getOrderNumber())
        ->format(FluidEmail::FORMAT_BOTH)  // HTML and plain text
        ->setTemplate('OrderConfirmation')
        ->assignMultiple([
            'order' => $order,
            'customer' => $order->getCustomer(),
        ]);

    $this->mailer->send($email);
}
```

### Plain Email

```php
use Symfony\Component\Mime\Email;

$email = GeneralUtility::makeInstance(Email::class);
$email
    ->from('sender@example.com')
    ->to('recipient@example.com')
    ->subject('Test Email')
    ->text('This is plain text email')
    ->html('<p>This is <strong>HTML</strong> email</p>');

$this->mailer->send($email);
```

## Translation API

### Translate Labels

```php
use TYPO3\CMS\Extbase\Utility\LocalizationUtility;

$translated = LocalizationUtility::translate(
    'product.label.title',  // Key
    'MyExtension'           // Extension key
);

// With arguments
$translated = LocalizationUtility::translate(
    'product.message.stockLow',
    'MyExtension',
    [$product->getStock()]  // Arguments for %s placeholders
);
```

### In Fluid Templates

```html
<f:translate key="product.label.title" extensionName="MyExtension" />

<!-- With arguments -->
<f:translate key="product.message.stockLow" arguments="{0: product.stock}" />
```

## Icon API

### Render Icons

```php
use TYPO3\CMS\Core\Imaging\IconFactory;
use TYPO3\CMS\Core\Imaging\Icon;

public function __construct(
    private readonly IconFactory $iconFactory
) {}

public function renderIcon(): string
{
    return $this->iconFactory->getIcon(
        'actions-document-save',
        Icon::SIZE_SMALL
    )->render();
}
```

### In Fluid Templates

```html
<core:icon identifier="actions-document-save" size="small" />
```

## Link Generation

### Generate Links in PHP

```php
use TYPO3\CMS\Core\Routing\RouterInterface;
use TYPO3\CMS\Backend\Routing\UriBuilder as BackendUriBuilder;
use TYPO3\CMS\Extbase\Mvc\Web\Routing\UriBuilder as FrontendUriBuilder;

// Backend module link
public function __construct(
    private readonly BackendUriBuilder $backendUriBuilder
) {}

$uri = $this->backendUriBuilder->buildUriFromRoute(
    'web_list',
    ['id' => 123]
);

// Frontend link in Extbase
public function buildLink(): string
{
    return $this->uriBuilder
        ->reset()
        ->setTargetPageUid(123)
        ->setArguments(['product' => $productId])
        ->build();
}
```

## JSON Response

### Return JSON in Controller

```php
public function ajaxAction(): ResponseInterface
{
    $data = [
        'success' => true,
        'products' => $this->productRepository->findAll(),
        'timestamp' => time(),
    ];

    return $this->jsonResponse(json_encode($data));
}
```

## Best Practices Summary

- ✅ **RequestFactory** - for HTTP requests (not `getUrl()` or raw cURL)
- ✅ **CacheManager** - for caching data
- ✅ **PSR-3 Logger** - for logging
- ✅ **FAL** - for file operations
- ✅ **Context API** - for getting current context
- ✅ **PSR-14 Events** - instead of old hooks
- ✅ **FlashMessages** - for user feedback
- ✅ **FluidEmail** - for sending emails
- ✅ **IconFactory** - for rendering icons
- ❌ **No deprecated APIs** - always use modern replacements

## References

- [TYPO3 Core API](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/)
- [RequestFactory](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Http/RequestFactory.html)
- [Caching Framework](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/CachingFramework/)
- [Logging](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Logging/)
- [FAL](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fal/)
- [PSR-14 Events](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/)
