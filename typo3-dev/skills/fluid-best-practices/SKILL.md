---
name: fluid-best-practices
description: Prevents business logic in Fluid templates and promotes proper ViewHelper usage. Use when working with Fluid templates, ViewHelpers, or frontend rendering.
---

# Fluid Best Practices Skill

Fluid is TYPO3's templating engine. Keep templates clean, semantic, and free of business logic.

## Core Principle: No Business Logic in Templates

Templates should only handle **presentation logic**, not **business logic**.

### ❌ Business Logic in Template (Avoid)

```html
<f:for each="{products}" as="product">
    <f:if condition="{product.stock} > 0">
        <f:if condition="{product.active}">
            <f:variable name="discountedPrice" value="{product.price * 0.9}" />
            <f:if condition="{discountedPrice} < 100">
                <div class="product product--sale">
                    <h3>{product.title}</h3>
                    <p class="price">
                        <f:format.currency>{discountedPrice}</f:format.currency>
                    </p>
                </div>
            </f:if>
        </f:if>
    </f:if>
</f:for>
```

### ✅ Presentation Logic Only (Preferred)

**Template:**
```html
<f:for each="{availableProducts}" as="product">
    <div class="product {f:if(condition: product.isOnSale, then: 'product--sale')}">
        <h3>{product.title}</h3>
        <p class="price">
            <f:format.currency>{product.displayPrice}</f:format.currency>
        </p>
        <f:if condition="{product.isOnSale}">
            <span class="badge">Sale!</span>
        </f:if>
    </div>
</f:for>
```

**Controller prepares data:**
```php
public function listAction(): ResponseInterface
{
    $products = $this->productService->getAvailableProducts();
    $this->view->assign('availableProducts', $products);
    return $this->htmlResponse();
}
```

**Model has presentation methods:**
```php
public function getDisplayPrice(): float
{
    return $this->isOnSale() ? $this->price * 0.9 : $this->price;
}

public function isOnSale(): bool
{
    return $this->displayPrice < 100;
}
```

## Template Structure

### Layouts

Layouts define the overall page structure:

**Resources/Private/Layouts/Default.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title><f:render section="title" /> - My Site</title>
    <f:asset.css identifier="main" href="EXT:my_ext/Resources/Public/Css/main.css" />
</head>
<body>
    <header>
        <f:render section="header" optional="true" />
    </header>

    <main>
        <f:render section="content" />
    </main>

    <footer>
        <f:render partial="Footer" />
    </footer>
</body>
</html>
```

### Templates

Templates use layouts and define sections:

**Resources/Private/Templates/Product/List.html:**
```html
<f:layout name="Default" />

<f:section name="title">Products</f:section>

<f:section name="content">
    <h1>Our Products</h1>

    <f:if condition="{products}">
        <f:then>
            <div class="product-grid">
                <f:for each="{products}" as="product">
                    <f:render partial="Product/Item" arguments="{product: product}" />
                </f:for>
            </div>
        </f:then>
        <f:else>
            <p>No products available.</p>
        </f:else>
    </f:if>
</f:section>
```

### Partials

Partials are reusable template snippets:

**Resources/Private/Partials/Product/Item.html:**
```html
<article class="product-item">
    <h3>{product.title}</h3>

    <f:if condition="{product.image}">
        <f:image image="{product.image}" width="300" />
    </f:if>

    <p class="price">
        <f:format.currency currencySign="€">{product.price}</f:format.currency>
    </p>

    <f:link.action action="show" arguments="{product: product}" class="btn">
        View Details
    </f:link.action>
</article>
```

## ViewHelpers Best Practices

### Using Built-in ViewHelpers

```html
{namespace f=TYPO3\CMS\Fluid\ViewHelpers}

<!-- Formatting -->
<f:format.currency currencySign="€">{price}</f:format.currency>
<f:format.date format="d.m.Y">{product.createdAt}</f:format.date>
<f:format.nl2br>{product.description}</f:format.nl2br>

<!-- Links -->
<f:link.action action="edit" arguments="{product: product}">Edit</f:link.action>
<f:link.page pageUid="123">About Us</f:link.page>
<f:link.external uri="https://example.com">External</f:link.external>

<!-- Forms -->
<f:form action="create" object="{newProduct}" name="product">
    <f:form.textfield property="title" />
    <f:form.textarea property="description" />
    <f:form.submit value="Save" />
</f:form>

<!-- Images -->
<f:image src="EXT:my_ext/Resources/Public/Images/logo.png" alt="Logo" />
<f:image image="{product.image}" width="300c" height="200c" />

<!-- Assets -->
<f:asset.css identifier="product-list" href="EXT:my_ext/Resources/Public/Css/products.css" />
<f:asset.script identifier="product-script" src="EXT:my_ext/Resources/Public/JavaScript/products.js" />
```

### Custom ViewHelpers

Create custom ViewHelpers for reusable presentation logic:

**Classes/ViewHelpers/Format/DiscountViewHelper.php:**
```php
<?php

declare(strict_types=1);

namespace Vendor\MyExt\ViewHelpers\Format;

use TYPO3Fluid\Fluid\Core\Rendering\RenderingContextInterface;
use TYPO3Fluid\Fluid\Core\ViewHelper\AbstractViewHelper;

final class DiscountViewHelper extends AbstractViewHelper
{
    public function initializeArguments(): void
    {
        $this->registerArgument('price', 'float', 'Original price', true);
        $this->registerArgument('rate', 'float', 'Discount rate (0-1)', true);
    }

    public static function renderStatic(
        array $arguments,
        \Closure $renderChildrenClosure,
        RenderingContextInterface $renderingContext
    ): float {
        $price = $arguments['price'];
        $rate = $arguments['rate'];

        return $price * (1 - $rate);
    }
}
```

**Usage in template:**
```html
{namespace v=Vendor\MyExt\ViewHelpers}

<f:format.currency>
    <v:format.discount price="{product.price}" rate="0.1" />
</f:format.currency>
```

### Inline ViewHelpers

For simple data transformations:

```html
{product.title -> f:format.htmlentities()}
{description -> f:format.crop(maxCharacters: 100)}
{price -> f:format.number(decimals: 2)}
```

## Security: Output Escaping

### Default Behavior

Fluid escapes all output by default (XSS protection):

```html
<!-- Automatically escaped -->
<p>{product.description}</p>
```

### Explicitly Disable Escaping (Dangerous!)

Only when absolutely necessary and content is trusted:

```html
<!-- Raw output - USE WITH CAUTION -->
<f:format.raw>{product.htmlContent}</f:format.raw>

<!-- OR -->
{product.htmlContent -> f:format.raw()}
```

⚠️ **Never** use `f:format.raw()` on user-generated content!

### Safe HTML Rendering

Use `f:format.html()` to parse RTE content safely:

```html
<f:format.html>{product.bodytext}</f:format.html>
```

## Conditions

### Simple Conditions

```html
<f:if condition="{product.stock} > 0">
    <span class="in-stock">In Stock</span>
</f:if>
```

### If-Then-Else

```html
<f:if condition="{user.isLoggedIn}">
    <f:then>
        <p>Welcome, {user.name}!</p>
    </f:then>
    <f:else>
        <p>Please log in.</p>
    </f:else>
</f:if>
```

### Inline If

```html
<div class="{f:if(condition: product.isNew, then: 'badge-new', else: 'badge-regular')}">
```

### Multiple Conditions

```html
<f:if condition="{product.stock} > 0 && {product.active}">
    <button>Add to Cart</button>
</f:if>
```

## Loops

### For Loop

```html
<f:for each="{products}" as="product" iteration="iterator">
    <div class="product {f:if(condition: iterator.isFirst, then: 'first')} {f:if(condition: iterator.isLast, then: 'last')}">
        <span class="index">{iterator.index}</span>
        <h3>{product.title}</h3>
    </div>
</f:for>
```

**Iterator properties:**
- `{iterator.index}` - 0-based index
- `{iterator.cycle}` - 1-based index
- `{iterator.isFirst}` - First item (boolean)
- `{iterator.isLast}` - Last item (boolean)
- `{iterator.isEven}` - Even index (boolean)
- `{iterator.isOdd}` - Odd index (boolean)
- `{iterator.total}` - Total count

### Grouping

```html
<f:groupedFor each="{products}" as="groupedProducts" groupBy="category" groupKey="categoryName">
    <h2>{categoryName}</h2>
    <f:for each="{groupedProducts}" as="product">
        <p>{product.title}</p>
    </f:for>
</f:groupedFor>
```

## Variables

```html
<!-- Set variable -->
<f:variable name="totalPrice" value="{product.price * product.quantity}" />

<!-- Use variable -->
<p>Total: <f:format.currency>{totalPrice}</f:format.currency></p>

<!-- Mathematical operations -->
<f:variable name="vat" value="{totalPrice * 0.19}" />
```

## Comments

```html
{# This is a Fluid comment - won't appear in HTML #}

<!-- This is an HTML comment - appears in source -->
```

## Debugging

```html
<!-- Debug single variable -->
<f:debug>{product}</f:debug>

<!-- Debug all variables -->
<f:debug>{_all}</f:debug>

<!-- Inline debugging -->
{product -> f:debug()}
```

⚠️ Remove debug statements before production!

## Common Mistakes to Avoid

### ❌ Complex Calculations

```html
<!-- Don't do math in templates -->
<p>Total: {product.price * quantity + (product.price * quantity * 0.19)}</p>
```

### ❌ Database Queries

```html
<!-- Never query database from template -->
<f:for each="{product.repository.findAll()}" as="item">
```

### ❌ Service Calls

```html
<!-- Don't call services from templates -->
<p>{productService.calculateDiscount(product)}</p>
```

### ❌ Nested Conditions

```html
<!-- Too complex - move to controller/model -->
<f:if condition="{user.isLoggedIn}">
    <f:if condition="{user.hasRole('admin')}">
        <f:if condition="{product.isPublished}">
            <f:if condition="{product.stock} > 0">
                <!-- ... -->
            </f:if>
        </f:if>
    </f:if>
</f:if>
```

### ✅ Move Logic to Controller/Model

```php
// Controller
$canOrder = $this->productService->canUserOrder($user, $product);
$this->view->assign('canOrder', $canOrder);
```

```html
<!-- Template -->
<f:if condition="{canOrder}">
    <button>Order Now</button>
</f:if>
```

## Performance Tips

1. **Minimize ViewHelper nesting** - Each ViewHelper has overhead
2. **Use Partials wisely** - Don't over-fragment templates
3. **Cache fragments** - Use `<f:cache.static>` for expensive renders
4. **Prepare data in controller** - Don't iterate/filter in templates
5. **Avoid debug in production** - Remove `<f:debug>` statements

## Best Practices Summary

- ✅ **No business logic** - Only presentation logic
- ✅ **Use Layouts/Partials** - Keep templates DRY
- ✅ **Prepare data in controller** - Templates just display
- ✅ **Custom ViewHelpers** - For reusable presentation logic
- ✅ **Output escaping** - Default is safe, be careful with `f:format.raw()`
- ✅ **Semantic HTML** - Clean, accessible markup
- ❌ **No calculations** - Do math in controller/model
- ❌ **No database access** - Query in controller/repository
- ❌ **No complex conditions** - Simplify in controller
- ❌ **No service calls** - Call from controller

## References

- [Fluid Templating Engine](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fluid/)
- [ViewHelper Reference](https://docs.typo3.org/other/typo3/view-helper-reference/main/en-us/)
- [Custom ViewHelpers](https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fluid/CustomViewHelpers.html)
