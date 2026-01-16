---
name: content-blocks
description: Guides creation of TYPO3 Content Blocks (v13+) - the modern way to create content elements. Use when creating custom content elements, page types, or record types.
---

# Content Blocks Skill

Content Blocks is the modern approach to creating custom content elements in TYPO3 v13+.

## What are Content Blocks?

Content Blocks replace the traditional way of creating content elements via TCA/TypoScript. They provide:
- YAML-based configuration
- Automatic TCA generation
- Automatic TypoScript generation
- Built-in backend previews
- Simpler developer experience

## Content Block Types

1. **Content Element** - Custom tt_content elements
2. **Page Type** - Custom page doktype
3. **Record Type** - Custom database records

## Directory Structure

```
ContentBlocks/
├── ContentElements/
│   └── my-element/
│       ├── EditorInterface.yaml    # Field configuration
│       ├── Source/
│       │   ├── Frontend.html       # Frontend template
│       │   ├── EditorPreview.html  # Backend preview
│       │   └── Language/
│       │       └── Labels.xlf      # Translations
│       └── Assets/
│           └── Icon.svg            # Content element icon
├── PageTypes/
│   └── my-page/
│       └── EditorInterface.yaml
└── RecordTypes/
    └── my-record/
        ├── EditorInterface.yaml
        └── Source/
            └── Language/
                └── Labels.xlf
```

## Creating a Content Element

### EditorInterface.yaml

```yaml
name: vendor/my-element
typeName: my_element
title: My Custom Element
description: A custom content element
group: common
prefixFields: true
prefixType: full

fields:
  - identifier: header
    useExistingField: true

  - identifier: headline
    type: Text
    label: Headline
    description: The main headline

  - identifier: text
    type: Textarea
    label: Text content
    enableRichtext: true

  - identifier: image
    type: File
    label: Image
    allowed: common-image-types
    maxitems: 1

  - identifier: link
    type: Link
    label: Link

  - identifier: items
    type: Collection
    label: Items
    foreign_table: tx_my_element_item
    fields:
      - identifier: title
        type: Text
        label: Title
      - identifier: description
        type: Textarea
        label: Description
```

### Frontend.html

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="my-element">
    <f:if condition="{data.headline}">
        <h2>{data.headline}</h2>
    </f:if>

    <f:if condition="{data.text}">
        <div class="my-element__text">
            <f:format.html>{data.text}</f:format.html>
        </div>
    </f:if>

    <f:if condition="{data.image}">
        <f:for each="{data.image}" as="image">
            <f:image image="{image}" width="800" alt="{image.alternative}" />
        </f:for>
    </f:if>

    <f:if condition="{data.link}">
        <a href="{f:uri.typolink(parameter: data.link)}" class="my-element__link">
            Learn more
        </a>
    </f:if>

    <f:if condition="{data.items}">
        <ul class="my-element__items">
            <f:for each="{data.items}" as="item">
                <li>
                    <strong>{item.title}</strong>
                    <p>{item.description}</p>
                </li>
            </f:for>
        </ul>
    </f:if>
</div>

</html>
```

### EditorPreview.html

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<div class="content-block-preview">
    <h3>{data.headline}</h3>
    <f:if condition="{data.text}">
        <p><f:format.crop maxCharacters="100">{data.text}</f:format.crop></p>
    </f:if>
    <f:if condition="{data.image}">
        <span class="badge">Has image</span>
    </f:if>
</div>

</html>
```

## Field Types Reference

| Type | Description | Options |
|------|-------------|---------|
| `Text` | Single line text | `max`, `placeholder`, `required` |
| `Textarea` | Multi-line text | `rows`, `enableRichtext` |
| `Number` | Numeric input | `range.lower`, `range.upper`, `format` |
| `Email` | Email field | - |
| `Link` | Link picker | `allowedTypes` |
| `Color` | Color picker | - |
| `DateTime` | Date/time picker | `format` |
| `File` | File reference | `allowed`, `maxitems` |
| `Folder` | Folder picker | - |
| `Category` | Category tree | - |
| `Select` | Dropdown | `items`, `renderType` |
| `Radio` | Radio buttons | `items` |
| `Checkbox` | Checkbox | - |
| `Collection` | Inline records | `fields`, `foreign_table` |
| `Relation` | Record relation | `foreign_table` |

## Field Configuration Examples

### Select Field
```yaml
- identifier: layout
  type: Select
  label: Layout
  default: default
  items:
    - label: Default
      value: default
    - label: Wide
      value: wide
    - label: Narrow
      value: narrow
```

### File with Validation
```yaml
- identifier: document
  type: File
  label: Document
  allowed: pdf,doc,docx
  maxitems: 5
  minitems: 1
```

### Relation to Pages
```yaml
- identifier: relatedPages
  type: Relation
  label: Related Pages
  foreign_table: pages
  maxitems: 3
```

## Using Existing Fields

```yaml
fields:
  # Use existing tt_content fields
  - identifier: header
    useExistingField: true

  - identifier: bodytext
    useExistingField: true

  - identifier: image
    useExistingField: true

  # Add custom fields
  - identifier: custom_field
    type: Text
    label: Custom Field
```

## Best Practices

1. **Naming Convention**
   - Use `vendor/element-name` format
   - Keep names descriptive but short

2. **Field Prefixing**
   - Use `prefixFields: true` to avoid conflicts
   - `prefixType: full` includes vendor name

3. **Translations**
   - Always provide Labels.xlf
   - Support multiple languages

4. **Icons**
   - Provide custom SVG icon
   - Use TYPO3 icon guidelines

5. **Backend Preview**
   - Always create EditorPreview.html
   - Show key content for editors

## Registering Content Blocks

In `ext_localconf.php` (usually automatic):

```php
// Content Blocks auto-registers in TYPO3 v13+
// Manual registration only needed for special cases
```

In `Configuration/ContentBlocks/` the blocks are auto-discovered.

## Migration from Traditional Content Elements

| Traditional | Content Block |
|-------------|---------------|
| TCA in `Configuration/TCA/Overrides/tt_content.php` | `EditorInterface.yaml` |
| TypoScript `tt_content.my_element` | Automatic |
| Fluid template in extension | `Source/Frontend.html` |
| Icon registration | `Assets/Icon.svg` |
| Language file | `Source/Language/Labels.xlf` |

## Resources

- [Content Blocks Documentation](https://docs.typo3.org/c/typo3/cms-content-blocks/main/en-us/)
- [Content Blocks Examples](https://github.com/TYPO3-Initiatives/content-blocks)
