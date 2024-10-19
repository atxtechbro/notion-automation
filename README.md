# Notion Automation

This repository automates the creation of databases and tasks in Notion using predefined JSON schema and tasks. It is optimized for extensibility and ease of use with minimal configuration.

## Core Magic ✨

- **Automates Notion task creation**: Define your tasks and schema in JSON, and let the automation do the heavy lifting.
- **Extensible & Customizable**: Plug-and-play JSON files for schema and task definitions.
- **Seamless API Integration**: Built-in Notion API integration for easy database creation.

## Quick Setup

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/your-repo/notion-automation.git
cd notion-automation
pip install -r requirements.txt
```

### 2. Configure Notion API

Create a `.env` file with your Notion API key and page ID:

```bash
NOTION_API_KEY=your_notion_api_key
NOTION_PAGE_ID=your_notion_page_id
```

### 3. Define Your Schema and Tasks

Store your schema and tasks in the `plugins/` folder. The schema defines the database structure, and the tasks define the content.

#### Example Schema (`schema.json`):

```json
{
  "title": "Project Tasks",
  "properties": [
    {
      "name": "Task Name",
      "type": "title"
    },
    {
      "name": "Due Date",
      "type": "date"
    },
    {
      "name": "Status",
      "type": "select",
      "options": [
        { "name": "To Do", "color": "red" },
        { "name": "In Progress", "color": "yellow" },
        { "name": "Done", "color": "green" }
      ]
    }
  ]
}
```

#### Example Tasks (`tasks.json`):

```json
{
  "tasks": [
    {
      "Task Name": "Implement feature X",
      "Due Date": "2023-10-15",
      "Status": "In Progress"
    },
    {
      "Task Name": "Fix bug Y",
      "Due Date": "2023-10-10",
      "Status": "To Do"
    }
  ]
}
```

### 4. Run the Magic 🪄

To create a database with tasks, run:

```bash
python cli.py --schema plugins/schema.json --tasks plugins/tasks.json
```

If you want to create an empty database without adding tasks, simply omit the --tasks argument:

```bash
python cli.py --schema plugins/schema.json
```

This will create a Notion database based on your schema without adding any tasks.

## Core Files

- **`cli.py`**: The main entry point for creating databases and tasks.
- **`notion_client/`**: Contains API integration logic and models.
- **`plugins/`**: Store your schema and task JSON files here. This folder is `.gitignore`d for privacy and customization.

## Logs & Debugging

Logs are automatically generated in `notion_automation.log`. Check the logs for detailed information on API calls and errors.
