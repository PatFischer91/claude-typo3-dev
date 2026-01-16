# TYPO3 Documentation MCP Server

Model Context Protocol (MCP) server for TYPO3 documentation access.

## Features

Provides tools for:
- **search_typo3_docs** - Search official TYPO3 documentation
- **get_typo3_changelog** - Fetch Core changelog entries
- **search_typo3_extensions** - Search TYPO3 Extension Repository (TER)
- **get_typo3_api_reference** - Get API reference for TYPO3 classes
- **get_typo3_coding_guidelines** - Retrieve coding guidelines

## Installation

```bash
cd mcp/typo3-docs-server
pip install -r requirements.txt
```

## Usage

This MCP server is automatically configured when the TYPO3 Development Plugin is installed.

### Manual Testing

```bash
python server.py
```

## Tools Reference

### search_typo3_docs

Search TYPO3 official documentation.

**Parameters:**
- `query` (required): Search term
- `version`: TYPO3 version (default: "main")
- `section`: Documentation section (default: "all")

**Example:**
```
Query: "QueryBuilder"
Version: "12.4"
Section: "reference-coreapi"
```

### get_typo3_changelog

Fetch changelog entries for version upgrades.

**Parameters:**
- `version` (required): TYPO3 version
- `type`: Entry type (Breaking, Deprecation, Feature, Important, All)
- `limit`: Max results (default: 10)

### search_typo3_extensions

Search TYPO3 Extension Repository.

**Parameters:**
- `query` (required): Search term
- `typo3_version`: Filter by compatibility
- `limit`: Max results

### get_typo3_api_reference

Get API documentation for TYPO3 classes.

**Parameters:**
- `class_name` (required): Fully qualified class name
- `method_name`: Specific method (optional)

### get_typo3_coding_guidelines

Retrieve coding guidelines for specific topic.

**Parameters:**
- `topic`: php, javascript, typescript, fluid, typoscript, database, security, all

## Development

This is a Python-based MCP server using the official MCP SDK.

**Key Components:**
- `server.py` - Main server implementation
- `requirements.txt` - Python dependencies

**MCP SDK Documentation:**
https://modelcontextprotocol.io/docs/develop/python

## License

MIT
