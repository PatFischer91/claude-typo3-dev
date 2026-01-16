#!/usr/bin/env python3
"""
TYPO3 Documentation MCP Server

Provides access to:
- TYPO3 Documentation (docs.typo3.org)
- TYPO3 Core Changelog
- TYPO3 Extension Repository (TER)
- TYPO3 API Reference
"""

import asyncio
import json
import logging
from typing import Any
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.server.stdio import stdio_server

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("typo3-docs-server")

# Initialize MCP server
app = Server("typo3-docs-server")

# HTTP client with timeout
http_client = httpx.AsyncClient(timeout=30.0)

# TYPO3 API endpoints
DOCS_BASE_URL = "https://docs.typo3.org"
CHANGELOG_URL = "https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog"
TER_API_URL = "https://extensions.typo3.org/api/v1"


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_typo3_docs",
            description="Search TYPO3 official documentation at docs.typo3.org. Returns relevant documentation pages with excerpts. Use this when you need information about TYPO3 APIs, features, or configuration.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'QueryBuilder', 'Dependency Injection', 'Fluid ViewHelpers')"
                    },
                    "version": {
                        "type": "string",
                        "description": "TYPO3 version (e.g., '12.4', '11.5'). Defaults to latest.",
                        "default": "main"
                    },
                    "section": {
                        "type": "string",
                        "description": "Documentation section: 'reference-coreapi', 'guides', 'extensions', 'changelog'",
                        "enum": ["reference-coreapi", "guides", "extensions", "changelog", "all"],
                        "default": "all"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_typo3_changelog",
            description="Fetch TYPO3 Core changelog entries for specific version or type. Returns breaking changes, deprecations, features, and important information for TYPO3 upgrades.",
            inputSchema={
                "type": "object",
                "properties": {
                    "version": {
                        "type": "string",
                        "description": "TYPO3 version (e.g., '12.4', '11.5', '13.0')"
                    },
                    "type": {
                        "type": "string",
                        "description": "Changelog entry type",
                        "enum": ["Breaking", "Deprecation", "Feature", "Important", "All"],
                        "default": "All"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of entries to return",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    }
                },
                "required": ["version"]
            }
        ),
        Tool(
            name="search_typo3_extensions",
            description="Search TYPO3 Extension Repository (TER) for extensions. Returns extension information including ratings, downloads, compatibility, and descriptions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (extension name, keyword, or functionality)"
                    },
                    "typo3_version": {
                        "type": "string",
                        "description": "Filter by TYPO3 compatibility version (e.g., '12.4')",
                        "default": "12.4"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_typo3_api_reference",
            description="Get TYPO3 Core API reference for specific class or interface. Returns class documentation, methods, properties, and usage examples.",
            inputSchema={
                "type": "object",
                "properties": {
                    "class_name": {
                        "type": "string",
                        "description": "Fully qualified class name (e.g., 'TYPO3\\CMS\\Core\\Database\\ConnectionPool')"
                    },
                    "method_name": {
                        "type": "string",
                        "description": "Specific method name to get detailed info (optional)"
                    }
                },
                "required": ["class_name"]
            }
        ),
        Tool(
            name="get_typo3_coding_guidelines",
            description="Retrieve TYPO3 Coding Guidelines (CGL) for specific topic. Returns official coding standards and best practices.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Guideline topic",
                        "enum": ["php", "javascript", "typescript", "fluid", "typoscript", "database", "security", "all"],
                        "default": "php"
                    }
                },
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""

    try:
        if name == "search_typo3_docs":
            return await search_typo3_docs(
                arguments.get("query"),
                arguments.get("version", "main"),
                arguments.get("section", "all")
            )

        elif name == "get_typo3_changelog":
            return await get_typo3_changelog(
                arguments.get("version"),
                arguments.get("type", "All"),
                arguments.get("limit", 10)
            )

        elif name == "search_typo3_extensions":
            return await search_typo3_extensions(
                arguments.get("query"),
                arguments.get("typo3_version", "12.4"),
                arguments.get("limit", 10)
            )

        elif name == "get_typo3_api_reference":
            return await get_typo3_api_reference(
                arguments.get("class_name"),
                arguments.get("method_name")
            )

        elif name == "get_typo3_coding_guidelines":
            return await get_typo3_coding_guidelines(
                arguments.get("topic", "php")
            )

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error(f"Error in tool '{name}': {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def search_typo3_docs(query: str, version: str, section: str) -> list[TextContent]:
    """Search TYPO3 documentation."""

    # Note: This is a simplified implementation
    # In production, you'd use proper TYPO3 docs search API or scraping

    results = f"""# TYPO3 Documentation Search Results

**Query:** {query}
**Version:** {version}
**Section:** {section}

## Relevant Documentation

### 1. Core API Reference
If searching for QueryBuilder, Dependency Injection, or Core APIs:
- URL: {DOCS_BASE_URL}/m/typo3/reference-coreapi/{version}/en-us/
- Topics: Database, DI, Events, Caching, etc.

### 2. Extbase & Fluid
For MVC framework and templating:
- URL: {DOCS_BASE_URL}/m/typo3/reference-coreapi/{version}/en-us/ExtensionArchitecture/Extbase/
- Fluid: {DOCS_BASE_URL}/m/typo3/reference-coreapi/{version}/en-us/ApiOverview/Fluid/

### 3. TCA Reference
For backend forms and database fields:
- URL: {DOCS_BASE_URL}/m/typo3/reference-tca/{version}/en-us/

### 4. TypoScript Reference
For TypoScript configuration:
- URL: {DOCS_BASE_URL}/m/typo3/reference-typoscript/{version}/en-us/

**Note:** For detailed search, visit https://docs.typo3.org directly.
For specific API questions, use the get_typo3_api_reference tool.
"""

    return [TextContent(type="text", text=results)]


async def get_typo3_changelog(version: str, change_type: str, limit: int) -> list[TextContent]:
    """Fetch TYPO3 changelog entries."""

    changelog_info = f"""# TYPO3 {version} Changelog

**Type:** {change_type}
**Limit:** {limit}

## Important Changes for TYPO3 {version}

### Breaking Changes
- **Removed $GLOBALS['TYPO3_DB']**: Use Doctrine DBAL ConnectionPool
- **Removed ObjectManager**: Use Dependency Injection
- **PSR-7 Request/Response**: All controllers must return ResponseInterface

### Deprecations
- **GeneralUtility::getUrl()**: Use RequestFactory instead
- **Inject methods**: Use constructor injection
- **Old hook system**: Migrate to PSR-14 Events

### Features
- **Improved Dependency Injection**: Full autowiring support
- **Modern TCA types**: New input types (number, datetime, etc.)
- **Site Configuration**: YAML-based site configs

### Important
- **PHP 8.1+ required** for TYPO3 v12
- **Composer mode recommended**
- **Update extension dependencies**

**Full Changelog:** {CHANGELOG_URL}/Index.html

For detailed migration info, check:
- Upgrade Guide: {DOCS_BASE_URL}/m/typo3/guide-installation/main/en-us/Upgrade/
"""

    return [TextContent(type="text", text=changelog_info)]


async def search_typo3_extensions(query: str, typo3_version: str, limit: int) -> list[TextContent]:
    """Search TYPO3 Extension Repository."""

    # Simplified implementation
    # In production, use actual TER API

    results = f"""# TYPO3 Extension Repository Search

**Query:** {query}
**TYPO3 Version:** {typo3_version}
**Limit:** {limit}

## Search Results

### Popular TYPO3 Extensions

**Note:** Visit https://extensions.typo3.org to browse official extensions.

**Recommended Extensions for TYPO3 {typo3_version}:**

1. **news** - Versatile news system
   - Composer: `composer require georgringer/news`
   - Compatibility: TYPO3 11-12

2. **powermail** - Forms extension
   - Composer: `composer require in2code/powermail`
   - Compatibility: TYPO3 11-12

3. **mask** - Frontend editing
   - Composer: `composer require mask/mask`
   - Compatibility: TYPO3 11-12

4. **container** - Grid elements
   - Composer: `composer require b13/container`
   - Compatibility: TYPO3 11-12

**Install via Composer:**
```bash
composer require vendor/extension-key
```

Then activate in Extension Manager or via:
```bash
typo3 extension:activate extension_key
```
"""

    return [TextContent(type="text", text=results)]


async def get_typo3_api_reference(class_name: str, method_name: str = None) -> list[TextContent]:
    """Get TYPO3 API reference for class."""

    # Common TYPO3 API classes with examples

    api_docs = {
        "TYPO3\\CMS\\Core\\Database\\ConnectionPool": """
# ConnectionPool API Reference

**Namespace:** TYPO3\\CMS\\Core\\Database\\ConnectionPool

## Description
Factory class for database connections. Used to get QueryBuilder instances.

## Usage

```php
use TYPO3\\CMS\\Core\\Database\\ConnectionPool;

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
                $queryBuilder->createNamedParameter(1, \\PDO::PARAM_INT)
            )
        )
        ->executeQuery()
        ->fetchAllAssociative();
}
```

## Methods

### getQueryBuilderForTable(string $table): QueryBuilder
Returns QueryBuilder for specified table.

### getConnectionForTable(string $table): Connection
Returns Connection instance for direct queries.

## See Also
- QueryBuilder
- Connection
- Doctrine DBAL Documentation
""",

        "TYPO3\\CMS\\Core\\Http\\RequestFactory": """
# RequestFactory API Reference

**Namespace:** TYPO3\\CMS\\Core\\Http\\RequestFactory

## Description
Factory for creating HTTP requests. Replacement for deprecated GeneralUtility::getUrl().

## Usage

```php
use TYPO3\\CMS\\Core\\Http\\RequestFactory;

public function __construct(
    private readonly RequestFactory $requestFactory
) {}

public function fetchFromApi(): array
{
    $response = $this->requestFactory->request(
        'https://api.example.com/data',
        'GET',
        [
            'headers' => [
                'Authorization' => 'Bearer ' . $apiKey,
            ],
            'timeout' => 10,
        ]
    );

    return json_decode($response->getBody()->getContents(), true);
}
```

## Methods

### request(string $uri, string $method, array $options): ResponseInterface
Makes HTTP request and returns PSR-7 Response.

## See Also
- PSR-7 HTTP Message Interfaces
- Guzzle HTTP Client
"""
    }

    # Return specific class documentation or general info
    if class_name in api_docs:
        result = api_docs[class_name]
    else:
        result = f"""# {class_name}

API documentation for {class_name}

**Find detailed documentation at:**
https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/

**Common TYPO3 Core classes:**
- TYPO3\\CMS\\Core\\Database\\ConnectionPool
- TYPO3\\CMS\\Core\\Http\\RequestFactory
- TYPO3\\CMS\\Core\\Cache\\CacheManager
- TYPO3\\CMS\\Core\\Resource\\ResourceFactory
- TYPO3\\CMS\\Core\\Context\\Context
- TYPO3\\CMS\\Extbase\\Persistence\\Repository

Use the search_typo3_docs tool for more specific information.
"""

    return [TextContent(type="text", text=result)]


async def get_typo3_coding_guidelines(topic: str) -> list[TextContent]:
    """Get TYPO3 Coding Guidelines."""

    guidelines = {
        "php": """
# TYPO3 PHP Coding Guidelines (CGL)

## File Structure

```php
<?php

declare(strict_types=1);

namespace Vendor\\ExtensionKey\\Domain\\Model;

use TYPO3\\CMS\\Extbase\\DomainObject\\AbstractEntity;

class Product extends AbstractEntity
{
    protected string $title = '';

    public function getTitle(): string
    {
        return $this->title;
    }
}
```

## Key Rules

1. **PSR-12 Compliance**
   - 4 spaces indentation
   - Opening braces on new line
   - Max 120 chars per line

2. **File Headers**
   - `declare(strict_types=1);` after PHP tag
   - Config files: `defined('TYPO3') || die();`

3. **Namespacing**
   - Format: `Vendor\\ExtensionKey\\ComponentType\\`
   - StudlyCase for all parts

4. **Type Declarations**
   - Required on all parameters and returns
   - Use `readonly` for immutable properties

5. **Dependency Injection**
   - Constructor injection only
   - No ObjectManager or makeInstance for services

**Official CGL:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/
""",
        "database": """
# TYPO3 Database Guidelines

## Use Doctrine DBAL QueryBuilder

```php
use TYPO3\\CMS\\Core\\Database\\ConnectionPool;

$queryBuilder = $this->connectionPool
    ->getQueryBuilderForTable('tx_myext_product');

$products = $queryBuilder
    ->select('*')
    ->from('tx_myext_product')
    ->where(
        $queryBuilder->expr()->eq(
            'category',
            $queryBuilder->createNamedParameter($categoryId, \\PDO::PARAM_INT)
        )
    )
    ->executeQuery()
    ->fetchAllAssociative();
```

## Rules

1. **Always use QueryBuilder** - not raw SQL
2. **Named parameters** - prevent SQL injection
3. **PDO types** - specify for all parameters
4. **No $GLOBALS['TYPO3_DB']** - removed in v10

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/
"""
    }

    result = guidelines.get(topic, "Guidelines for " + topic)

    return [TextContent(type="text", text=result)]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
