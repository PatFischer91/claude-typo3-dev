#!/usr/bin/env python3
"""
TYPO3 Documentation MCP Server

Provides access to:
- TYPO3 Documentation (docs.typo3.org)
- TYPO3 Core Changelog
- TYPO3 Extension Repository (TER) - Real API
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
http_client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

# TYPO3 API endpoints
DOCS_BASE_URL = "https://docs.typo3.org"
DOCS_SEARCH_URL = "https://docs.typo3.org/services/ajaxsearch/"
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
                        "description": "TYPO3 version (e.g., '12.4', '11.5'). Defaults to main.",
                        "default": "main"
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
                        "default": "12"
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
            name="get_extension_detail",
            description="Get detailed information about a specific TYPO3 extension from TER.",
            inputSchema={
                "type": "object",
                "properties": {
                    "extension_key": {
                        "type": "string",
                        "description": "The extension key (e.g., 'news', 'powermail', 'mask')"
                    }
                },
                "required": ["extension_key"]
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
                arguments.get("version", "main")
            )

        elif name == "get_typo3_changelog":
            return await get_typo3_changelog(
                arguments.get("version"),
                arguments.get("type", "All")
            )

        elif name == "search_typo3_extensions":
            return await search_typo3_extensions(
                arguments.get("query"),
                arguments.get("typo3_version", "12"),
                arguments.get("limit", 10)
            )

        elif name == "get_extension_detail":
            return await get_extension_detail(
                arguments.get("extension_key")
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


async def search_typo3_docs(query: str, version: str) -> list[TextContent]:
    """Search TYPO3 documentation using the docs.typo3.org search."""

    try:
        # TYPO3 docs uses Algolia for search - we can query the search service
        search_url = f"{DOCS_SEARCH_URL}?q={query}"

        response = await http_client.get(search_url)

        if response.status_code == 200:
            try:
                data = response.json()
                results = []

                if "results" in data and data["results"]:
                    results.append(f"# TYPO3 Documentation Search: {query}\n")
                    results.append(f"**Version:** {version}\n\n")

                    for i, item in enumerate(data["results"][:10], 1):
                        title = item.get("title", "No title")
                        url = item.get("url", "")
                        snippet = item.get("snippet", item.get("description", ""))

                        results.append(f"## {i}. {title}\n")
                        if url:
                            results.append(f"**URL:** {url}\n")
                        if snippet:
                            results.append(f"{snippet}\n")
                        results.append("\n")

                    return [TextContent(type="text", text="".join(results))]
            except json.JSONDecodeError:
                pass

        # Fallback: provide manual search guidance
        return await _fallback_docs_search(query, version)

    except Exception as e:
        logger.error(f"Error searching docs: {str(e)}")
        return await _fallback_docs_search(query, version)


async def _fallback_docs_search(query: str, version: str) -> list[TextContent]:
    """Fallback documentation search with curated links."""

    # Map common queries to relevant documentation URLs
    doc_mapping = {
        "querybuilder": ("Database", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/"),
        "database": ("Database", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/"),
        "dependency injection": ("Dependency Injection", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/DependencyInjection/"),
        "di": ("Dependency Injection", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/DependencyInjection/"),
        "fluid": ("Fluid Templating", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fluid/"),
        "viewhelper": ("ViewHelpers", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fluid/ViewHelper/"),
        "tca": ("TCA Reference", "/m/typo3/reference-tca/main/en-us/"),
        "typoscript": ("TypoScript Reference", "/m/typo3/reference-typoscript/main/en-us/"),
        "extbase": ("Extbase", "/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/"),
        "controller": ("Controllers", "/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/Reference/Controller/"),
        "repository": ("Repositories", "/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/Reference/Domain/Repository/"),
        "model": ("Domain Models", "/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/Reference/Domain/Model/"),
        "event": ("Events", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/"),
        "psr-14": ("PSR-14 Events", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Events/"),
        "middleware": ("Middleware", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/RequestHandling/"),
        "caching": ("Caching", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/CachingFramework/"),
        "logging": ("Logging", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Logging/"),
        "fal": ("File Abstraction Layer", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fal/"),
        "security": ("Security", "/m/typo3/reference-coreapi/main/en-us/Security/"),
        "site": ("Site Configuration", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/SiteHandling/"),
        "routing": ("Routing", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Routing/"),
        "backend": ("Backend Development", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Backend/"),
        "form": ("Form Framework", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/FormFramework/"),
        "scheduler": ("Scheduler", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/Scheduler/"),
        "command": ("CLI Commands", "/m/typo3/reference-coreapi/main/en-us/ApiOverview/CommandControllers/"),
    }

    query_lower = query.lower()
    matched_docs = []

    for keyword, (title, path) in doc_mapping.items():
        if keyword in query_lower:
            matched_docs.append((title, f"{DOCS_BASE_URL}{path}"))

    result = f"""# TYPO3 Documentation Search: {query}

**Version:** {version}

## Relevant Documentation

"""

    if matched_docs:
        for title, url in matched_docs:
            result += f"### {title}\n**URL:** {url}\n\n"
    else:
        result += f"""No exact matches found. Try these resources:

### Core API Reference
**URL:** {DOCS_BASE_URL}/m/typo3/reference-coreapi/{version}/en-us/

### TCA Reference
**URL:** {DOCS_BASE_URL}/m/typo3/reference-tca/{version}/en-us/

### TypoScript Reference
**URL:** {DOCS_BASE_URL}/m/typo3/reference-typoscript/{version}/en-us/

### Extbase & Fluid
**URL:** {DOCS_BASE_URL}/m/typo3/reference-coreapi/{version}/en-us/ExtensionArchitecture/Extbase/

"""

    result += f"""
**Direct Search:** https://docs.typo3.org/search/?q={query}
"""

    return [TextContent(type="text", text=result)]


async def get_typo3_changelog(version: str, change_type: str) -> list[TextContent]:
    """Fetch TYPO3 changelog entries."""

    # Extract major version
    major_version = version.split(".")[0] if "." in version else version

    changelog_base = f"https://docs.typo3.org/c/typo3/cms-core/{major_version}.4/en-us/Changelog"

    result = f"""# TYPO3 {version} Changelog

**Type Filter:** {change_type}
**Changelog URL:** {changelog_base}/Index.html

## Version-Specific Changes

"""

    # Version-specific information (curated)
    version_changes = {
        "11": {
            "Breaking": [
                "Removed TypoScript conditions using old syntax (globalVar, etc.)",
                "Removed support for PHP 7.2 and 7.3",
                "Removed GeneralUtility::_GP(), _GET(), _POST()",
            ],
            "Deprecation": [
                "ObjectManager usage deprecated in favor of DI",
                "switchableControllerActions deprecated",
                "Many TypoScript settings moved to site configuration",
            ],
            "Feature": [
                "Full Symfony DI container support",
                "Site configuration for languages",
                "Modern TCA improvements",
            ]
        },
        "12": {
            "Breaking": [
                "ObjectManager removed - use Dependency Injection",
                "All controller actions MUST return ResponseInterface",
                "$GLOBALS['TSFE'] direct access removed - use request attributes",
                "switchableControllerActions removed",
                "PHP 8.1+ required",
            ],
            "Deprecation": [
                "GeneralUtility::getUrl() - use RequestFactory",
                "Old hook system - use PSR-14 Events",
                "TCA type 'input' with eval='int' - use type 'number'",
                "TCA type 'input' with renderType='inputDateTime' - use type 'datetime'",
            ],
            "Feature": [
                "New TCA types: number, datetime, email, link, password, color, uuid",
                "Improved backend UI",
                "Full PSR-14 event system",
                "Doctrine DBAL 3.x",
            ]
        },
        "13": {
            "Breaking": [
                "PHP 8.2+ required",
                "Composer-only installation",
                "Many deprecated features removed",
            ],
            "Deprecation": [
                "Legacy backend modules",
                "Old content element wizards",
            ],
            "Feature": [
                "Content Blocks - new way to create content elements",
                "Site Sets for configuration management",
                "New backend UI components",
                "Improved security features",
            ]
        }
    }

    if major_version in version_changes:
        changes = version_changes[major_version]

        if change_type == "All":
            for ctype, items in changes.items():
                result += f"### {ctype} Changes\n"
                for item in items:
                    result += f"- {item}\n"
                result += "\n"
        elif change_type in changes:
            result += f"### {change_type} Changes\n"
            for item in changes[change_type]:
                result += f"- {item}\n"
    else:
        result += f"No curated changelog available for version {version}.\n"
        result += f"Please visit: {changelog_base}/Index.html\n"

    result += f"""
## Useful Links

- **Full Changelog:** {changelog_base}/Index.html
- **Upgrade Guide:** https://docs.typo3.org/m/typo3/guide-installation/main/en-us/Upgrade/
- **Breaking Changes:** {changelog_base}/Breaking/Index.html
- **Deprecations:** {changelog_base}/Deprecation/Index.html
"""

    return [TextContent(type="text", text=result)]


async def search_typo3_extensions(query: str, typo3_version: str, limit: int) -> list[TextContent]:
    """Search TYPO3 Extension Repository using real API."""

    try:
        # Real TER API endpoint for search
        search_url = f"{TER_API_URL}/extension/search/?q={query}&typo3Version={typo3_version}&limit={limit}"

        response = await http_client.get(search_url)

        if response.status_code == 200:
            data = response.json()

            result = f"""# TYPO3 Extension Search: {query}

**TYPO3 Version:** {typo3_version}
**Results:** {len(data.get('extensions', []))} found

## Extensions

"""

            extensions = data.get("extensions", [])
            if extensions:
                for ext in extensions[:limit]:
                    key = ext.get("key", "unknown")
                    title = ext.get("title", key)
                    description = ext.get("description", "No description")[:200]
                    downloads = ext.get("downloads", 0)
                    version = ext.get("currentVersion", {}).get("version", "unknown")
                    author = ext.get("author", {}).get("name", "Unknown")

                    result += f"""### {title} ({key})

**Version:** {version} | **Downloads:** {downloads:,}
**Author:** {author}

{description}

**Install:** `composer require typo3-ter/{key}`
**TER:** https://extensions.typo3.org/extension/{key}

---

"""
            else:
                result += "No extensions found matching your search.\n"

            return [TextContent(type="text", text=result)]

    except Exception as e:
        logger.error(f"TER API error: {str(e)}")

    # Fallback with popular extensions
    return await _fallback_extension_search(query, typo3_version)


async def _fallback_extension_search(query: str, typo3_version: str) -> list[TextContent]:
    """Fallback extension search with popular extensions."""

    popular_extensions = {
        "news": ("News System", "georgringer/news", "Versatile news system with categories, tags, and more"),
        "powermail": ("Powermail", "in2code/powermail", "Powerful form extension with many features"),
        "mask": ("Mask", "mask/mask", "Create custom content elements without coding"),
        "container": ("Container", "b13/container", "Create container elements for content"),
        "solr": ("Solr", "apache-solr-for-typo3/solr", "Apache Solr integration for TYPO3"),
        "tt_address": ("Address", "friendsoftypo3/tt-address", "Address management extension"),
        "realurl": ("RealURL", "-", "Deprecated - use native TYPO3 routing instead"),
        "form": ("Form", "Built-in", "Native TYPO3 form framework (part of core)"),
        "seo": ("SEO", "Built-in", "Native TYPO3 SEO features (part of core since v9)"),
    }

    result = f"""# TYPO3 Extension Search: {query}

**TYPO3 Version:** {typo3_version}

## Popular Extensions

"""

    query_lower = query.lower()
    for key, (title, composer, desc) in popular_extensions.items():
        if query_lower in key or query_lower in title.lower() or query_lower in desc.lower():
            result += f"""### {title} ({key})

{desc}

**Composer:** `composer require {composer}`
**TER:** https://extensions.typo3.org/extension/{key}

---

"""

    result += f"""
## Search TER Directly

For more extensions, visit:
https://extensions.typo3.org/?search={query}
"""

    return [TextContent(type="text", text=result)]


async def get_extension_detail(extension_key: str) -> list[TextContent]:
    """Get detailed extension information from TER."""

    try:
        detail_url = f"{TER_API_URL}/extension/{extension_key}"
        response = await http_client.get(detail_url)

        if response.status_code == 200:
            ext = response.json()

            current_version = ext.get("currentVersion", {})

            result = f"""# {ext.get('title', extension_key)}

**Extension Key:** {extension_key}
**Current Version:** {current_version.get('version', 'unknown')}
**Downloads:** {ext.get('downloads', 0):,}
**Category:** {ext.get('category', 'unknown')}

## Description

{ext.get('description', 'No description available')}

## Author

**Name:** {ext.get('author', {}).get('name', 'Unknown')}
**Company:** {ext.get('author', {}).get('company', '-')}

## Compatibility

**TYPO3:** {current_version.get('typo3Dependency', 'Check documentation')}
**PHP:** {current_version.get('phpDependency', 'Check documentation')}

## Installation

```bash
composer require typo3-ter/{extension_key}
```

Or via Extension Manager in TYPO3 Backend.

## Links

- **TER:** https://extensions.typo3.org/extension/{extension_key}
- **Documentation:** {ext.get('documentationLink', 'Check TER page')}
- **Repository:** {ext.get('repositoryUrl', 'Check TER page')}
"""

            return [TextContent(type="text", text=result)]

    except Exception as e:
        logger.error(f"Extension detail error: {str(e)}")

    return [TextContent(type="text", text=f"Could not fetch details for extension '{extension_key}'. Visit: https://extensions.typo3.org/extension/{extension_key}")]


async def get_typo3_api_reference(class_name: str, method_name: str = None) -> list[TextContent]:
    """Get TYPO3 API reference for class."""

    # Comprehensive API documentation
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
Returns QueryBuilder for specified table with proper restrictions.

### getConnectionForTable(string $table): Connection
Returns raw Connection instance for direct queries.

### getConnectionByName(string $name): Connection
Returns Connection by configured name.

## Documentation
https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/
""",

        "TYPO3\\CMS\\Core\\Http\\RequestFactory": """
# RequestFactory API Reference

**Namespace:** TYPO3\\CMS\\Core\\Http\\RequestFactory

## Description
Factory for creating HTTP requests. Replacement for deprecated GeneralUtility::getUrl().

## Usage

```php
use TYPO3\\CMS\\Core\\Http\\RequestFactory;
use Psr\\Http\\Message\\ResponseInterface;

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

## Methods

### request(string $uri, string $method = 'GET', array $options = []): ResponseInterface
Makes HTTP request and returns PSR-7 Response.

## Options
- `headers` - Array of HTTP headers
- `timeout` - Request timeout in seconds
- `query` - Query parameters
- `body` - Request body
- `form_params` - Form data (POST)
- `json` - JSON body

## Documentation
https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Http/
""",

        "TYPO3\\CMS\\Extbase\\Mvc\\Controller\\ActionController": """
# ActionController API Reference

**Namespace:** TYPO3\\CMS\\Extbase\\Mvc\\Controller\\ActionController

## Description
Base class for Extbase controllers. All plugin controllers should extend this.

## Usage

```php
<?php

declare(strict_types=1);

namespace Vendor\\MyExtension\\Controller;

use Psr\\Http\\Message\\ResponseInterface;
use TYPO3\\CMS\\Extbase\\Mvc\\Controller\\ActionController;
use Vendor\\MyExtension\\Domain\\Repository\\ProductRepository;

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

## Important Methods

### htmlResponse(?string $html = null): ResponseInterface
Returns HTML response. Must be used in TYPO3 v12+.

### jsonResponse(?string $json = null): ResponseInterface
Returns JSON response.

### redirect(...): ResponseInterface
Redirects to another action.

### forward(...): void
Forwards to another action without redirect.

## Properties

- `$this->request` - Current request
- `$this->view` - View instance
- `$this->settings` - Plugin settings from TypoScript

## Documentation
https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/Reference/Controller/
""",

        "TYPO3\\CMS\\Extbase\\Persistence\\Repository": """
# Repository API Reference

**Namespace:** TYPO3\\CMS\\Extbase\\Persistence\\Repository

## Description
Base class for Extbase repositories. Handles all data persistence.

## Usage

```php
<?php

declare(strict_types=1);

namespace Vendor\\MyExtension\\Domain\\Repository;

use TYPO3\\CMS\\Extbase\\Persistence\\Repository;
use TYPO3\\CMS\\Extbase\\Persistence\\QueryInterface;

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

## Methods

### findAll(): QueryResultInterface
Returns all objects.

### findByUid(int $uid): ?object
Returns object by UID.

### add(object $object): void
Adds new object.

### update(object $object): void
Updates existing object.

### remove(object $object): void
Removes object.

### createQuery(): QueryInterface
Creates query for custom queries.

## Documentation
https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ExtensionArchitecture/Extbase/Reference/Domain/Repository/
"""
    }

    if class_name in api_docs:
        return [TextContent(type="text", text=api_docs[class_name])]

    # Generic response for unknown classes
    result = f"""# {class_name}

API documentation for `{class_name}`

## Find Documentation

The class might be documented at:
https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/

## Common TYPO3 Core Classes

Use `get_typo3_api_reference` with these class names:

- `TYPO3\\CMS\\Core\\Database\\ConnectionPool` - Database queries
- `TYPO3\\CMS\\Core\\Http\\RequestFactory` - HTTP requests
- `TYPO3\\CMS\\Extbase\\Mvc\\Controller\\ActionController` - Controllers
- `TYPO3\\CMS\\Extbase\\Persistence\\Repository` - Repositories

## PHP Docs

For API documentation, check the TYPO3 source code or use IDE autocompletion.
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
    protected float $price = 0.0;

    public function getTitle(): string
    {
        return $this->title;
    }

    public function setTitle(string $title): void
    {
        $this->title = $title;
    }

    public function getPrice(): float
    {
        return $this->price;
    }
}
```

## Key Rules

### 1. PSR-12 Compliance
- 4 spaces indentation (no tabs)
- Opening braces on new line for classes/methods
- Max 120 chars per line
- Single quotes for strings

### 2. File Headers
- `declare(strict_types=1);` after PHP tag
- Config files: `defined('TYPO3') || die();`

### 3. Namespacing
- Format: `Vendor\\ExtensionKey\\ComponentType\\`
- StudlyCase for all parts

### 4. Type Declarations
- Required on all parameters and returns
- Use `readonly` for immutable properties (PHP 8.1+)

### 5. Dependency Injection
- Constructor injection only
- `private readonly` for dependencies
- No ObjectManager or makeInstance for services

### 6. Naming Conventions
- Classes: StudlyCase
- Methods: camelCase
- Properties: camelCase
- Constants: UPPER_SNAKE_CASE

**Official CGL:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/
""",

        "database": """
# TYPO3 Database Guidelines

## Use Doctrine DBAL QueryBuilder

```php
use TYPO3\\CMS\\Core\\Database\\ConnectionPool;
use TYPO3\\CMS\\Core\\Database\\Connection;

public function __construct(
    private readonly ConnectionPool $connectionPool
) {}

public function findActiveProducts(int $categoryId): array
{
    $queryBuilder = $this->connectionPool
        ->getQueryBuilderForTable('tx_myext_product');

    return $queryBuilder
        ->select('uid', 'title', 'price')
        ->from('tx_myext_product')
        ->where(
            $queryBuilder->expr()->eq(
                'category',
                $queryBuilder->createNamedParameter($categoryId, Connection::PARAM_INT)
            ),
            $queryBuilder->expr()->eq(
                'active',
                $queryBuilder->createNamedParameter(1, Connection::PARAM_INT)
            )
        )
        ->orderBy('title', 'ASC')
        ->executeQuery()
        ->fetchAllAssociative();
}
```

## Key Rules

1. **Always use QueryBuilder** - never raw SQL strings
2. **Named parameters** - always use createNamedParameter()
3. **PDO types** - specify Connection::PARAM_INT, PARAM_STR, etc.
4. **No $GLOBALS['TYPO3_DB']** - removed since TYPO3 v10
5. **Never concatenate user input** - SQL injection risk

## IN() Clause Example

```php
$queryBuilder
    ->where(
        $queryBuilder->expr()->in(
            'category',
            $queryBuilder->createNamedParameter(
                $categoryIds,
                Connection::PARAM_INT_ARRAY
            )
        )
    )
```

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Database/
""",

        "fluid": """
# TYPO3 Fluid Guidelines

## Template Structure

```
Resources/Private/
├── Layouts/
│   └── Default.html
├── Templates/
│   └── Product/
│       ├── List.html
│       └── Show.html
└── Partials/
    └── Product/
        └── Item.html
```

## Template Example

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default" />

<f:section name="main">
    <div class="products">
        <f:for each="{products}" as="product">
            <f:render partial="Product/Item" arguments="{product: product}" />
        </f:for>
    </div>
</f:section>

</html>
```

## Key Rules

1. **No business logic** - only presentation
2. **Use ViewHelpers** for complex logic
3. **Never f:format.raw() on user input** - XSS risk
4. **Prepare data in Controller** - not in template
5. **Use Layouts and Partials** - DRY principle

## Security

```html
<!-- GOOD: Escaped by default -->
{product.title}

<!-- DANGEROUS: Only use for trusted HTML -->
<f:format.raw>{trustedHtml}</f:format.raw>

<!-- GOOD: Proper link handling -->
<f:link.typolink parameter="{product.link}">Read more</f:link.typolink>
```

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Fluid/
""",

        "security": """
# TYPO3 Security Guidelines

## Input Validation

```php
// GOOD: Use typed parameters
public function showAction(int $productId): ResponseInterface

// GOOD: Validate input
if ($productId <= 0) {
    throw new \\InvalidArgumentException('Invalid product ID');
}
```

## Database Security

```php
// GOOD: Named parameters
$queryBuilder->expr()->eq(
    'uid',
    $queryBuilder->createNamedParameter($uid, Connection::PARAM_INT)
)

// BAD: String concatenation (SQL Injection!)
$queryBuilder->where("uid = " . $uid)
```

## Output Security

```html
<!-- GOOD: Escaped by default -->
{userInput}

<!-- BAD: XSS vulnerability -->
<f:format.raw>{userInput}</f:format.raw>
```

## File Upload Security

```php
// Validate file type
$allowedTypes = ['image/jpeg', 'image/png'];
if (!in_array($file->getMimeType(), $allowedTypes, true)) {
    throw new \\InvalidArgumentException('Invalid file type');
}

// Validate file size
if ($file->getSize() > 5 * 1024 * 1024) {
    throw new \\InvalidArgumentException('File too large');
}
```

## Key Rules

1. **Never trust user input** - always validate
2. **Use QueryBuilder** with named parameters
3. **Escape output** - Fluid does this by default
4. **Validate file uploads** - type, size, content
5. **No sensitive data in logs** - passwords, tokens
6. **Use HTTPS** in production
7. **CSRF protection** - use backend modules properly

**Docs:** https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/Security/
""",

        "typoscript": """
# TYPO3 TypoScript Guidelines

## File Structure

```
Configuration/
├── TypoScript/
│   ├── constants.typoscript
│   ├── setup.typoscript
│   └── Includes/
│       └── Plugin.typoscript
```

## Setup Example

```typoscript
plugin.tx_myextension {
    view {
        templateRootPaths.10 = EXT:my_extension/Resources/Private/Templates/
        partialRootPaths.10 = EXT:my_extension/Resources/Private/Partials/
        layoutRootPaths.10 = EXT:my_extension/Resources/Private/Layouts/
    }

    persistence {
        storagePid = {$plugin.tx_myextension.persistence.storagePid}
    }

    settings {
        itemsPerPage = {$plugin.tx_myextension.settings.itemsPerPage}
    }
}
```

## Constants Example

```typoscript
plugin.tx_myextension {
    persistence {
        # cat=plugin.tx_myextension/storage/010; type=int; label=Storage PID
        storagePid = 1
    }

    settings {
        # cat=plugin.tx_myextension/settings/010; type=int; label=Items per page
        itemsPerPage = 10
    }
}
```

## Key Rules

1. **Use constants** for configurable values
2. **Proper file extension** - .typoscript (not .ts or .txt)
3. **Include via @import** - not INCLUDE_TYPOSCRIPT
4. **Use EXT: prefix** for extension paths
5. **Comment complex logic**

**Docs:** https://docs.typo3.org/m/typo3/reference-typoscript/main/en-us/
""",

        "all": """
# TYPO3 Coding Guidelines Overview

## Quick Reference

### PHP
- PSR-12 compliance
- `declare(strict_types=1);`
- Constructor DI with `private readonly`
- Type declarations everywhere

### Database
- Always QueryBuilder
- Always createNamedParameter()
- Never concatenate SQL

### Fluid
- No business logic
- Data prepared in Controller
- Use ViewHelpers for complex logic
- Escaping by default

### Security
- Validate all input
- QueryBuilder with named params
- No f:format.raw() on user input
- Validate file uploads

### TypoScript
- Use constants
- .typoscript extension
- EXT: for paths
- @import for includes

## Official Documentation

https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/CodingGuidelines/
"""
    }

    result = guidelines.get(topic, guidelines["all"])
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
