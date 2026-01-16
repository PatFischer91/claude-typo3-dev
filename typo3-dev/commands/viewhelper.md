---
description: Creates a custom TYPO3 Fluid ViewHelper with proper structure, type hints, and documentation
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Create TYPO3 Fluid ViewHelper

Generates a custom ViewHelper following TYPO3 best practices.

## Usage

```
/typo3:viewhelper <ViewHelperName> [type]
```

**Parameters:**
- `ViewHelperName`: ViewHelper name in StudlyCase (e.g., `FormatPrice`, `RenderStatus`)
- `type`: Optional type - `static` (default) or `instance`

**Arguments:** $ARGUMENTS

## Steps

### 1. Detect Extension Context

- Look for `ext_emconf.php` or `composer.json`
- Extract extension key and vendor name
- Determine namespace

### 2. Parse Arguments

- Extract ViewHelper name
- Determine ViewHelper category from name (Format, Render, Link, etc.)
- Choose static or instance-based rendering

### 3. Create ViewHelper Directory Structure

Organize by category if applicable:
- `Classes/ViewHelpers/Format/PriceViewHelper.php`
- `Classes/ViewHelpers/Link/ProductViewHelper.php`
- `Classes/ViewHelpers/Widget/PaginationViewHelper.php`

Or flat structure:
- `Classes/ViewHelpers/<ViewHelperName>ViewHelper.php`

### 4. Generate Static ViewHelper (Recommended)

**Path:** `Classes/ViewHelpers/<ViewHelperName>ViewHelper.php`

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\ViewHelpers;

use TYPO3Fluid\Fluid\Core\Rendering\RenderingContextInterface;
use TYPO3Fluid\Fluid\Core\ViewHelper\AbstractViewHelper;
use TYPO3Fluid\Fluid\Core\ViewHelper\Traits\CompileWithRenderStatic;

/**
 * <ViewHelperName> ViewHelper
 *
 * Usage:
 * <code>
 * <v:<viewhelpername> argument="value" />
 * </code>
 *
 * Or inline:
 * <code>
 * {value -> v:<viewhelpername>()}
 * </code>
 */
final class <ViewHelperName>ViewHelper extends AbstractViewHelper
{
    use CompileWithRenderStatic;

    /**
     * Disable escaping of output (set to true if returning HTML)
     */
    protected $escapeOutput = true;

    /**
     * Initialize arguments
     */
    public function initializeArguments(): void
    {
        parent::initializeArguments();

        $this->registerArgument(
            'value',
            'mixed',
            'The value to process',
            false,
            null
        );

        // Add more arguments:
        // $this->registerArgument(
        //     'format',
        //     'string',
        //     'Output format',
        //     false,
        //     'default'
        // );
    }

    /**
     * Render the ViewHelper
     *
     * @param array<string, mixed> $arguments
     * @param \Closure $renderChildrenClosure
     * @param RenderingContextInterface $renderingContext
     * @return mixed
     */
    public static function renderStatic(
        array $arguments,
        \Closure $renderChildrenClosure,
        RenderingContextInterface $renderingContext
    ): mixed {
        $value = $arguments['value'] ?? $renderChildrenClosure();

        if ($value === null) {
            return '';
        }

        // Your ViewHelper logic here
        // Example: return strtoupper((string)$value);

        return $value;
    }
}
```

### 5. Generate Instance ViewHelper (When Needed)

Use instance-based when you need:
- Access to `$this->renderChildren()`
- Complex state management
- Injection of services

```php
<?php

declare(strict_types=1);

namespace <VendorName>\<ExtensionKey>\ViewHelpers;

use TYPO3Fluid\Fluid\Core\ViewHelper\AbstractViewHelper;

/**
 * <ViewHelperName> ViewHelper (Instance-based)
 */
final class <ViewHelperName>ViewHelper extends AbstractViewHelper
{
    protected $escapeOutput = true;

    public function initializeArguments(): void
    {
        parent::initializeArguments();

        $this->registerArgument('value', 'mixed', 'The value to process', false, null);
    }

    /**
     * Render the ViewHelper
     */
    public function render(): mixed
    {
        $value = $this->arguments['value'] ?? $this->renderChildren();

        if ($value === null) {
            return '';
        }

        // Your ViewHelper logic here
        return $value;
    }
}
```

### 6. Common ViewHelper Examples

**Format/PriceViewHelper.php:**
```php
public static function renderStatic(
    array $arguments,
    \Closure $renderChildrenClosure,
    RenderingContextInterface $renderingContext
): string {
    $value = $arguments['value'] ?? $renderChildrenClosure();
    $currency = $arguments['currency'] ?? '€';
    $decimals = $arguments['decimals'] ?? 2;

    return number_format((float)$value, $decimals, ',', '.') . ' ' . $currency;
}
```

**Format/TruncateViewHelper.php:**
```php
public static function renderStatic(
    array $arguments,
    \Closure $renderChildrenClosure,
    RenderingContextInterface $renderingContext
): string {
    $value = (string)($arguments['value'] ?? $renderChildrenClosure());
    $maxLength = (int)$arguments['maxLength'];
    $suffix = $arguments['suffix'] ?? '...';

    if (mb_strlen($value) <= $maxLength) {
        return $value;
    }

    return mb_substr($value, 0, $maxLength) . $suffix;
}
```

### 7. Register Namespace in Templates

In Fluid templates, register the namespace:

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:v="http://typo3.org/ns/<VendorName>/<ExtensionKey>/ViewHelpers"
      data-namespace-typo3-fluid="true">
```

Or with `{namespace}`:

```html
{namespace v=<VendorName>\<ExtensionKey>\ViewHelpers}
```

## Best Practices Applied

1. **Use Static Rendering**
   - `renderStatic()` with `CompileWithRenderStatic` trait
   - Better performance through compilation
   - Only use instance-based when necessary

2. **Proper Argument Registration**
   - All arguments in `initializeArguments()`
   - Clear type, description, required flag, default value

3. **Output Escaping**
   - `$escapeOutput = true` by default (safe)
   - Set to `false` only when returning trusted HTML

4. **No Business Logic**
   - ViewHelpers for presentation only
   - Complex logic belongs in services

5. **Type Safety**
   - Strict types enabled
   - Proper type hints on all methods

## Success Message

```
✓ ViewHelper '<ViewHelperName>ViewHelper' created!

File created:
- Classes/ViewHelpers/<ViewHelperName>ViewHelper.php

Usage in templates:

1. Register namespace:
   xmlns:v="http://typo3.org/ns/<VendorName>/<ExtensionKey>/ViewHelpers"

2. Use tag syntax:
   <v:<viewhelpername> value="{myValue}" />

3. Or inline syntax:
   {myValue -> v:<viewhelpername>()}

Next steps:
1. Implement your logic in renderStatic()
2. Add more arguments if needed
3. Clear cache: typo3 cache:flush
```
