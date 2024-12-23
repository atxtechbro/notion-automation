# Notion Automation

A custom implementation for automating Notion database operations. This package provides direct API integration without relying on the official `notion-client` package.

## Important Note

This package is a standalone implementation and is **not** related to the official `notion-client` package. We've built our own client to:
- Have more control over the API interactions
- Implement custom schema handling
- Provide simplified database operations

## Setup

1. Create a `.env` file with your Notion credentials:
```bash
NOTION_API_KEY=your-api-key-here
NOTION_PAGE_ID=your-page-id-here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Creating a Database

1. Create a schema file in `plugins/` (e.g., `football_schema.json`):
```json
{
    "title": "College Football Games",
    "properties": {
        "Game": {
            "property_type": "title",
            "name": "Game"
        },
        "Status": {
            "property_type": "select",
            "name": "Status",
            "options": [
                {
                    "name": "Scheduled"
                },
                {
                    "name": "In Progress"
                },
                {
                    "name": "Final"
                }
            ]
        }
    }
}
```

2. Create entries file (e.g., `football_games.json`):
```json
{
    "entries": [
        {
            "Game": "Rose Bowl - Alabama vs Michigan",
            "Status": "Scheduled"
        }
    ]
}
```

3. Run the CLI:
```bash
python -m notion_automation.cli create --schema plugins/football_schema.json --tasks plugins/football_games.json
```

### Getting Database Schema

Retrieve schema of an existing database:
```bash
python -m notion_automation.cli get-schema --id your-database-id
```

## Supported Property Types

- `title`: Database title field
- `rich_text`: Multi-line text field
- `select`: Single-select with options
- `date`: Date field

## Project Structure

- `notion_automation/`
  - `cli.py`: Command-line interface
  - `models.py`: Data models for database configuration
  - `notion_client/`: Notion API client implementation
  - `logger.py`: Logging configuration

## Development

- Configuration files go in `plugins/` directory (gitignored)
- Logs are written to `notion_automation.log`
- Debug level logging available for API payloads

## Logging

Three log levels are used:
- DEBUG: Detailed API payloads and responses
- INFO: General operation success
- ERROR: API errors and exceptions

Logs are written to both console and `notion_automation.log` file.

## Implementation Details

This package includes:
- Custom Notion API client (`notion_automation.notion_client`)
- Schema validation and parsing
- Database creation and management
- No dependencies on external Notion client libraries

## Contributing

When contributing, note that this package:
1. Uses its own Notion API client implementation
2. Does not depend on the official `notion-client` package
3. Handles all API interactions directly
