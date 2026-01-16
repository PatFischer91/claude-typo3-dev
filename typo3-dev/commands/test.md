---
description: Creates Unit or Functional tests for TYPO3 classes using the TYPO3 Testing Framework
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Create TYPO3 Tests

Generates Unit or Functional tests using the TYPO3 Testing Framework.

## Usage

```
/typo3:test <TestName> [type]
```

**Parameters:**
- `TestName`: Test class name or class to test (e.g., `ProductService`, `ProductServiceTest`)
- `type`: Test type - `unit` (default) or `functional`

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Look for `ext_emconf.php` or `composer.json`
- Extract extension key and vendor name
- Find the class to test (if exists)

### 2. Parse Arguments

- Extract test name (add "Test" suffix if needed)
- Determine test type (unit/functional)
- Find corresponding class to test

### 3. Create Test Directory Structure

```
Tests/
├── Unit/
│   ├── Controller/
│   ├── Domain/
│   │   ├── Model/
│   │   └── Repository/
│   └── Service/
└── Functional/
    ├── Controller/
    └── Repository/
```

### 4. Generate Unit Test

**Path:** `Tests/Unit/<Path>/<TestName>Test.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Tests\Unit\<Path>;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Unit\UnitTestCase;
use <VendorName>\<ExtensionKey>\<Path>\<ClassName>;

/**
 * Test case for <ClassName>
 */
final class <ClassName>Test extends UnitTestCase
{
    protected bool $resetSingletonInstances = true;

    private <ClassName> $subject;

    protected function setUp(): void
    {
        parent::setUp();

        // Create mocks for dependencies
        // $mockRepository = $this->createMock(ProductRepository::class);

        // Create subject with mocked dependencies
        $this->subject = new <ClassName>(
            // $mockRepository
        );
    }

    protected function tearDown(): void
    {
        parent::tearDown();
        unset($this->subject);
    }

    #[Test]
    public function constructorCreatesInstance(): void
    {
        self::assertInstanceOf(<ClassName>::class, $this->subject);
    }

    #[Test]
    public function exampleMethodReturnsExpectedResult(): void
    {
        // Arrange
        $input = 'test input';
        $expected = 'expected output';

        // Act
        // $result = $this->subject->exampleMethod($input);

        // Assert
        // self::assertSame($expected, $result);
        self::assertTrue(true); // Placeholder
    }

    #[Test]
    public function exampleMethodThrowsExceptionOnInvalidInput(): void
    {
        // $this->expectException(\InvalidArgumentException::class);
        // $this->expectExceptionCode(1234567890);

        // $this->subject->exampleMethod(null);
        self::assertTrue(true); // Placeholder
    }
}
```

### 5. Generate Functional Test

**Path:** `Tests/Functional/<Path>/<TestName>Test.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Tests\Functional\<Path>;

use PHPUnit\Framework\Attributes\Test;
use TYPO3\TestingFramework\Core\Functional\FunctionalTestCase;
use <VendorName>\<ExtensionKey>\<Path>\<ClassName>;

/**
 * Functional test case for <ClassName>
 */
final class <ClassName>Test extends FunctionalTestCase
{
    /**
     * Extensions to load
     */
    protected array $testExtensionsToLoad = [
        'typo3conf/ext/<extension_key>',
    ];

    /**
     * Core extensions to load
     */
    protected array $coreExtensionsToLoad = [
        'extbase',
        'fluid',
    ];

    private <ClassName> $subject;

    protected function setUp(): void
    {
        parent::setUp();

        // Import database fixtures
        $this->importCSVDataSet(__DIR__ . '/Fixtures/<ClassName>.csv');

        // Get subject from container
        $this->subject = $this->get(<ClassName>::class);
    }

    #[Test]
    public function findAllReturnsExpectedRecords(): void
    {
        // $result = $this->subject->findAll();

        // self::assertCount(3, $result);
        self::assertTrue(true); // Placeholder
    }

    #[Test]
    public function findByUidReturnsCorrectRecord(): void
    {
        // $result = $this->subject->findByUid(1);

        // self::assertNotNull($result);
        // self::assertSame('Test Title', $result->getTitle());
        self::assertTrue(true); // Placeholder
    }

    #[Test]
    public function createPersistsRecord(): void
    {
        // Arrange
        // $newItem = new Product();
        // $newItem->setTitle('New Product');

        // Act
        // $this->subject->add($newItem);
        // $this->persistenceManager->persistAll();

        // Assert
        // $this->assertCSVDataSet(__DIR__ . '/Assertions/CreatePersistsRecord.csv');
        self::assertTrue(true); // Placeholder
    }
}
```

### 6. Create Test Fixtures (Functional Tests)

**Path:** `Tests/Functional/<Path>/Fixtures/<ClassName>.csv`

```csv
"tx_<extensionkey>_domain_model_<modelname>"
,"uid","pid","title","description","hidden","deleted"
,1,1,"Test Item 1","Description 1",0,0
,2,1,"Test Item 2","Description 2",0,0
,3,1,"Test Item 3","Description 3",0,0
```

### 7. Generate Test Utilities

**Path:** `Tests/Unit/Fixtures/MockTrait.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\Tests\Unit\Fixtures;

trait MockTrait
{
    protected function createProductMock(array $properties = []): Product
    {
        $mock = $this->createMock(Product::class);

        foreach ($properties as $property => $value) {
            $getter = 'get' . ucfirst($property);
            $mock->method($getter)->willReturn($value);
        }

        return $mock;
    }
}
```

### 8. Configure PHPUnit

**Path:** `Tests/phpunit.xml` (if not exists)

```xml
<?xml version="1.0"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/10.5/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/UnitTestsBootstrap.php"
         colors="true"
         beStrictAboutTestsThatDoNotTestAnything="false">

    <testsuites>
        <testsuite name="Unit Tests">
            <directory>Tests/Unit/</directory>
        </testsuite>
    </testsuites>

    <coverage>
        <report>
            <html outputDirectory=".Build/coverage"/>
        </report>
    </coverage>

    <source>
        <include>
            <directory suffix=".php">Classes/</directory>
        </include>
    </source>
</phpunit>
```

### 9. Update composer.json

Add to `composer.json`:

```json
{
    "require-dev": {
        "typo3/testing-framework": "^8.0"
    },
    "autoload-dev": {
        "psr-4": {
            "<VendorName>\\<ExtensionKey>\\Tests\\": "Tests/"
        }
    }
}
```

## Common Test Patterns

### Testing Services with Mocks

```php
#[Test]
public function processOrderSendsEmail(): void
{
    $mailServiceMock = $this->createMock(MailService::class);
    $mailServiceMock
        ->expects(self::once())
        ->method('send')
        ->with(self::isInstanceOf(Order::class));

    $subject = new OrderService($mailServiceMock);
    $subject->processOrder($this->createOrderMock());
}
```

### Testing Repository Queries

```php
#[Test]
public function findActiveReturnsOnlyActiveProducts(): void
{
    // Import test data with mixed active/inactive products
    $this->importCSVDataSet(__DIR__ . '/Fixtures/MixedProducts.csv');

    $result = $this->subject->findActive();

    self::assertCount(2, $result);
    foreach ($result as $product) {
        self::assertTrue($product->isActive());
    }
}
```

## Success Message

```
✓ Test '<TestName>Test' created!

Files created:
- Tests/<Type>/<Path>/<TestName>Test.php
- Tests/<Type>/<Path>/Fixtures/<TestName>.csv (functional only)

Run tests:
  Unit:       vendor/bin/phpunit -c Tests/phpunit.xml Tests/Unit/
  Functional: vendor/bin/phpunit -c Tests/phpunit.xml Tests/Functional/

Or with TYPO3 Testing Framework:
  .Build/bin/phpunit -c Build/phpunit/UnitTests.xml

Next steps:
1. Install testing-framework: composer require --dev typo3/testing-framework
2. Implement actual test assertions
3. Add more test cases
4. Run tests to verify
```
