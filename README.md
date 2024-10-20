# Notion Automation

This repository automates the creation of databases and entries in Notion using predefined JSON schemas and entry definitions. It is optimized for extensibility and ease of use with minimal configuration.

## Core Magic ✨

- **Automates Notion data entry**: Define your entries and schema in JSON, and let the automation do the heavy lifting.
- **Extensible & Customizable**: Plug-and-play JSON files for schema and entry definitions.
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

### 3. Define Your Schema and Entries

Store your schema and entries (optional) in the `plugins/` folder. The schema defines the database structure, and the entries define the content.

#### Example Schema (`schema.json`):

```json
{
  "title": "Project Entities",
  "properties": [
    {
      "name": "Name",
      "type": "title"
    },
    {
      "name": "Type",
      "type": "select",
      "options": [
        { "name": "Entity", "color": "blue" },
        { "name": "Component", "color": "green" },
        { "name": "Module", "color": "purple" }
      ]
    },
    {
      "name": "Created At",
      "type": "date"
    },
    {
      "name": "Tags",
      "type": "multi_select",
      "options": [
        { "name": "Core", "color": "red" },
        { "name": "Active", "color": "green" },
        { "name": "Archived", "color": "gray" },
        { "name": "Reference", "color": "yellow" }
      ]
    }
  ]
}
```

#### Example Entries (`entries.json`):

```json
{
  "entries": [
    {
      "Name": "Alpha",
      "Type": "Entity",
      "Created At": "2023-10-15",
      "Tags": ["Core", "Active"]
    },
    {
      "Name": "Beta",
      "Type": "Entity",
      "Created At": "2023-10-10",
      "Tags": ["Archived", "Reference"]
    }
  ]
}
```

### 4. Run the Magic 🪄

To create a database with preseeded entries, run:

```bash
python cli.py --schema plugins/schema.json --entries plugins/entries.json
```

If you want to create an empty database without adding entries, simply omit the --entries argument:

```bash
python cli.py --schema plugins/schema.json
```

This will create a Notion database based on your schema without adding any entries.

## Core Files

- **`cli.py`**: The main entry point for creating databases and entries.
- **`notion_client/`**: Contains API integration logic and models.
- **`plugins/`**: Store your schema and entry JSON files here. This folder is `.gitignore`d for privacy and customization.

## Logs & Debugging

Logs are automatically generated in `notion_automation.log`. Check the logs for detailed information on API calls and errors.
