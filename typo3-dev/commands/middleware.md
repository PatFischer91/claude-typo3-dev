---
description: Creates a PSR-15 compliant TYPO3 Middleware with proper registration and dependency injection
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Create TYPO3 PSR-15 Middleware

Generates a PSR-15 compliant Middleware with proper structure and registration.

## Usage

```
/typo3:middleware <MiddlewareName> [stack]
```

**Parameters:**
- `MiddlewareName`: Middleware name in StudlyCase (e.g., `Authentication`, `JsonResponse`)
- `stack`: Optional stack - `frontend` (default) or `backend`

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Look for `ext_emconf.php` or `composer.json`
- Extract extension key and vendor name
- Determine namespace

### 2. Parse Arguments

- Extract middleware name
- Determine stack (frontend/backend)

### 3. Generate Middleware Class

**Path:** `Classes/Middleware/<MiddlewareName>Middleware.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Middleware;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;
use Psr\Log\LoggerInterface;

/**
 * <MiddlewareName> Middleware
 *
 * This middleware handles <description>.
 */
final class <MiddlewareName>Middleware implements MiddlewareInterface
{
    public function __construct(
        private readonly LoggerInterface $logger,
        // Add more dependencies here
    ) {}

    /**
     * Process the request
     *
     * @param ServerRequestInterface $request
     * @param RequestHandlerInterface $handler
     * @return ResponseInterface
     */
    public function process(
        ServerRequestInterface $request,
        RequestHandlerInterface $handler
    ): ResponseInterface {
        // PRE-PROCESSING
        // Modify request or perform checks before the main handler

        // Example: Log incoming request
        $this->logger->debug('<MiddlewareName> middleware processing', [
            'uri' => (string)$request->getUri(),
            'method' => $request->getMethod(),
        ]);

        // Example: Add custom attribute to request
        // $request = $request->withAttribute('custom_attribute', 'value');

        // Example: Early return (block request)
        // if ($this->shouldBlock($request)) {
        //     return new \TYPO3\CMS\Core\Http\JsonResponse(
        //         ['error' => 'Access denied'],
        //         403
        //     );
        // }

        // CALL NEXT HANDLER
        $response = $handler->handle($request);

        // POST-PROCESSING
        // Modify response after the main handler

        // Example: Add custom header
        // $response = $response->withHeader('X-Custom-Header', 'value');

        return $response;
    }
}
```

### 4. Register Middleware

**Path:** `Configuration/RequestMiddlewares.php`

```php
<?php

return [
    'frontend' => [
        '<vendorname>/<extensionkey>/<middlewarename>' => [
            'target' => \<VendorName>\<ExtensionKey>\Middleware\<MiddlewareName>Middleware::class,
            'description' => '<MiddlewareName> middleware description',
            'before' => [
                'typo3/cms-frontend/page-resolver',
            ],
            'after' => [
                'typo3/cms-frontend/site',
            ],
        ],
    ],
];
```

For backend middleware:

```php
<?php

return [
    'backend' => [
        '<vendorname>/<extensionkey>/<middlewarename>' => [
            'target' => \<VendorName>\<ExtensionKey>\Middleware\<MiddlewareName>Middleware::class,
            'description' => '<MiddlewareName> middleware for backend',
            'before' => [
                'typo3/cms-backend/authentication',
            ],
        ],
    ],
];
```

### 5. Common Middleware Patterns

**Authentication Middleware:**
```php
public function process(
    ServerRequestInterface $request,
    RequestHandlerInterface $handler
): ResponseInterface {
    $authHeader = $request->getHeaderLine('Authorization');

    if (!$this->isValidToken($authHeader)) {
        return new JsonResponse(['error' => 'Unauthorized'], 401);
    }

    $userId = $this->extractUserId($authHeader);
    $request = $request->withAttribute('authenticated_user', $userId);

    return $handler->handle($request);
}
```

**CORS Middleware:**
```php
public function process(
    ServerRequestInterface $request,
    RequestHandlerInterface $handler
): ResponseInterface {
    // Handle preflight request
    if ($request->getMethod() === 'OPTIONS') {
        return $this->createCorsResponse();
    }

    $response = $handler->handle($request);

    // Add CORS headers
    return $response
        ->withHeader('Access-Control-Allow-Origin', '*')
        ->withHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        ->withHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
}
```

**JSON Response Middleware:**
```php
public function process(
    ServerRequestInterface $request,
    RequestHandlerInterface $handler
): ResponseInterface {
    // Only process API routes
    $path = $request->getUri()->getPath();
    if (!str_starts_with($path, '/api/')) {
        return $handler->handle($request);
    }

    try {
        $response = $handler->handle($request);
        return $response;
    } catch (\Throwable $e) {
        $this->logger->error('API error', ['exception' => $e]);
        return new JsonResponse([
            'error' => $e->getMessage(),
        ], 500);
    }
}
```

### 6. TYPO3 Middleware Stack Reference

**Frontend Stack (order):**
1. `typo3/cms-core/normalized-params-attribute`
2. `typo3/cms-frontend/timetracker`
3. `typo3/cms-frontend/site`
4. `typo3/cms-frontend/authentication`
5. `typo3/cms-frontend/page-resolver`
6. `typo3/cms-frontend/prepare-tsfe-rendering`

**Backend Stack (order):**
1. `typo3/cms-core/normalized-params-attribute`
2. `typo3/cms-backend/locked-backend`
3. `typo3/cms-backend/authentication`
4. `typo3/cms-backend/site-resolver`

## Best Practices Applied

1. **PSR-15 Compliance**
   - Implements `MiddlewareInterface`
   - Proper `process()` signature
   - Returns `ResponseInterface`

2. **Dependency Injection**
   - Services via constructor
   - Use `private readonly`
   - No static calls

3. **Request Modification**
   - Use `withAttribute()` for adding data
   - Immutable request handling

4. **Proper Positioning**
   - `before`/`after` for ordering
   - Choose correct stack (frontend/backend)

## Success Message

```
✓ Middleware '<MiddlewareName>Middleware' created!

Files created:
- Classes/Middleware/<MiddlewareName>Middleware.php
- Configuration/RequestMiddlewares.php (created/updated)

Middleware registered in: <stack> stack

Next steps:
1. Implement your middleware logic
2. Adjust before/after positioning if needed
3. Clear cache: typo3 cache:flush
4. Test middleware execution

Middleware order can be checked via:
typo3 configuration:showlist --type=HTTP/Middlewares
```
