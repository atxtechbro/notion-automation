# Notion Automation

Tool for automating Notion database creation and management using JSON schemas.

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
