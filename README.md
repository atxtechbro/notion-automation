# Notion Automation

This repository provides scripts and configurations to automate task creation in Notion, designed for extensibility.

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
   Run the script using a JSON schema from `config/database_configs/`:
   ```bash
   python -m scripts.create_database your_config_name
   ```

## Configuration

- **Database schemas** and **tasks** are defined in JSON files within `config/database_configs/`. Customize schemas to fit your use case.
  
### Example JSON Schema:
```json
{
  "title": "Project Tasks",
  "properties": {
    "Name": { "property_type": "title" },
    "Status": { "property_type": "select", "options": [{"name": "To Do"}] }
  },
  "tasks": [
    {
      "properties": {
        "Name": { "type": "title", "value": "Task 1" },
        "Status": { "type": "select", "value": "To Do" }
      }
    }
  ]
}
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