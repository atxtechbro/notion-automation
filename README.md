```md
# Notion Automation

This repository provides scripts and configurations to automate task creation in Notion. It is designed for extensibility and easily configurable to fit various use cases.

## Quick Start

1. **Clone the repo & install dependencies:**
   ```bash
   git clone https://github.com/atxtechbro/notion-automation.git
   cd notion-automation
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Add your Notion API key and page ID to a `.env` file:
   ```bash
   NOTION_API_KEY=your_notion_api_key
   NOTION_PAGE_ID=your_notion_page_id
   ```

3. **Create a database:**
   Use the `create_database` command to create a Notion database by specifying the JSON schema and tasks. Example:
   ```bash
   python cli.py create_database --schema path/to/schema.json --tasks path/to/tasks.json
   ```

## Example JSON Schema and Tasks

You can define the database schema and tasks in any directory and pass their paths as arguments when creating the database. Here's an example of what the JSON files could look like:

### Example Schema JSON (`schema.json`):
```json
{
  "title": "Daily Tasks",
  "properties": {
    "Name": { "property_type": "title" },
    "Status": { "property_type": "select", "options": [{"name": "To Do"}, {"name": "In Progress"}, {"name": "Done"}] }
  }
}
```

### Example Tasks JSON (`tasks.json`):
```json
{
  "tasks": [
    {
      "properties": {
        "Name": { "type": "title", "value": "Finish regression testing at work" },
        "Status": { "type": "select", "value": "To Do" }
      }
    },
    {
      "properties": {
        "Name": { "type": "title", "value": "Reach out to at least three orgs about siphon utility" },
        "Status": { "type": "select", "value": "To Do" }
      }
    },
    {
      "properties": {
        "Name": { "type": "title", "value": "Workout" },
        "Status": { "type": "select", "value": "To Do" }
      }
    },
    {
      "properties": {
        "Name": { "type": "title", "value": "Say a prayer and have quiet time" },
        "Status": { "type": "select", "value": "To Do" }
      }
    }
  ]
}
```

4. **Run the script:**
   ```bash
   python cli.py create_database --schema schema.json --tasks tasks.json
   ```

## Run Tests

Run all tests using `pytest`:
```bash
pytest
```

## Logging

Logs are saved to `notion_automation.log` for debugging.

## Contribute

Submit pull requests or issues to help enhance this automation toolkit.
```

### New CLI Usage

Instead of pointing users to the `config/database_configs/` directory that no longer exists, the usage should guide them to use custom paths for their schema and tasks JSON files when running the `create_database` script.

For example:
- Command to create a database:  
   ```bash
   python cli.py create_database --schema path/to/schema.json --tasks path/to/tasks.json
   ```
- Make sure the `.env` file is configured with the correct API keys for Notion.

This updated approach reflects the removal of the old directory structure and replaces it with a CLI-based method where users provide their own schema and tasks files from any location.
