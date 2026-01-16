---
description: Creates a PSR-14 Event class and EventListener for TYPO3 with proper registration in Services.yaml
allowed-tools: Read, Write, Edit, Glob
---

# Create TYPO3 PSR-14 Event

Generates a PSR-14 Event class and EventListener.

## Usage

```
/typo3:event <EventName> [properties]
```

**Parameters:**
- `EventName`: Event name in StudlyCase (e.g., `ProductCreated`, `OrderProcessed`)
- `properties`: Optional comma-separated properties (e.g., `product:Product,user:int`)

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Find extension key and vendor name
- Determine namespace

### 2. Generate Event Class

**Path:** `Classes/Event/<EventName>Event.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Event;

/**
 * <EventName> Event
 *
 * Dispatched when <description>.
 */
final class <EventName>Event
{
    public function __construct(
        private readonly mixed $subject,
        private readonly array $data = []
    ) {}

    /**
     * Get the subject of the event
     */
    public function getSubject(): mixed
    {
        return $this->subject;
    }

    /**
     * Get additional event data
     */
    public function getData(): array
    {
        return $this->data;
    }

    /**
     * Get a specific data value
     */
    public function get(string $key, mixed $default = null): mixed
    {
        return $this->data[$key] ?? $default;
    }
}
```

### 3. Generate Event Listener

**Path:** `Classes/EventListener/<EventName>Listener.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\EventListener;

use <VendorName>\<ExtensionKey>\Event\<EventName>Event;
use Psr\Log\LoggerInterface;

/**
 * Listener for <EventName>Event
 */
final class <EventName>Listener
{
    public function __construct(
        private readonly LoggerInterface $logger
    ) {}

    /**
     * Handle the event
     */
    public function __invoke(<EventName>Event $event): void
    {
        $subject = $event->getSubject();

        $this->logger->info('<EventName> event received', [
            'subject' => $subject,
            'data' => $event->getData(),
        ]);

        // Add your event handling logic here
    }
}
```

### 4. Register Listener in Services.yaml

Add to `Configuration/Services.yaml`:

```yaml
services:
  <VendorName>\<ExtensionKey>\EventListener\<EventName>Listener:
    tags:
      - name: event.listener
        identifier: '<extension_key>-<eventname>-listener'
        event: <VendorName>\<ExtensionKey>\Event\<EventName>Event
```

### 5. Dispatch Event Example

In your service or controller:

```php
use Psr\EventDispatcher\EventDispatcherInterface;
use <VendorName>\<ExtensionKey>\Event\<EventName>Event;

class ProductService
{
    public function __construct(
        private readonly EventDispatcherInterface $eventDispatcher
    ) {}

    public function createProduct(array $data): Product
    {
        $product = new Product();
        // ... create product

        // Dispatch event
        $event = new <EventName>Event($product, [
            'createdBy' => $this->getCurrentUser(),
            'timestamp' => time(),
        ]);
        $this->eventDispatcher->dispatch($event);

        return $product;
    }
}
```

### 6. Common TYPO3 Core Events

You can also listen to TYPO3 Core events:

```yaml
# Listen to Core events
services:
  <VendorName>\<ExtensionKey>\EventListener\PageLoadedListener:
    tags:
      - name: event.listener
        event: TYPO3\CMS\Frontend\Event\AfterCacheableContentIsGeneratedEvent

  <VendorName>\<ExtensionKey>\EventListener\ModifyQueryListener:
    tags:
      - name: event.listener
        event: TYPO3\CMS\Core\Database\Event\AlterTableDefinitionStatementsEvent
```

**Common Core Events:**
- `AfterCacheableContentIsGeneratedEvent`
- `BeforePageIsResolvedEvent`
- `ModifyRecordListTableActionsEvent`
- `ModifyUrlForCanonicalTagEvent`
- `AfterFileAddedEvent`
- `BeforeFileDeletedEvent`

## Stoppable Events

For events that can be stopped:

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Event;

use Psr\EventDispatcher\StoppableEventInterface;

final class <EventName>Event implements StoppableEventInterface
{
    private bool $propagationStopped = false;

    public function isPropagationStopped(): bool
    {
        return $this->propagationStopped;
    }

    public function stopPropagation(): void
    {
        $this->propagationStopped = true;
    }
}
```

## Success Message

```
✓ PSR-14 Event '<EventName>Event' created!

Files created:
- Classes/Event/<EventName>Event.php
- Classes/EventListener/<EventName>Listener.php
- Configuration/Services.yaml (updated)

Dispatch event:
$this->eventDispatcher->dispatch(new <EventName>Event($subject, $data));

Next steps:
1. Customize event properties
2. Add event handling logic in listener
3. Clear cache: typo3 cache:flush
```
