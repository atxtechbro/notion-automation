# Notion Automation

This repository contains scripts and configurations to automate task creation in Notion. It is designed to be extensible for future automations.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/atxtechbro/notion-automation.git
   cd notion-automation
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root of the repository and add your Notion API key and the Notion page ID where the database will be created:
   ```env
   NOTION_API_KEY=your_notion_api_key
   NOTION_PAGE_ID=your_notion_page_id
   ```

5. **Ensure your directory structure is as follows:**
   ```
   notion-automation/
   ├── venv/
   ├── scripts/
   │   ├── __init__.py
   │   └── create_database.py
   ├── config/
   │   └── database_configs/
   │       └── gym_strength_ifbb_training.json
   ├── .env
   ├── requirements.txt
   └── main.py
   ```

6. **Run the script:**
   ```bash
   python -m scripts.create_database gym_strength_ifbb_training
   ```

### Example Usage

To create a database using the `gym_strength_ifbb_training` configuration, use the following command:
```bash
python -m scripts.create_database gym_strength_ifbb_training
```

This will create a Notion database and tasks based on the `gym_strength_ifbb_training.json` configuration file located in the `config/database_configs/` directory.

### Notes

- Ensure that your Notion API key and page ID are correctly set in the `.env` file.
- The JSON configuration files should be placed in the `config/database_configs/` directory.
- You can add more configurations by creating additional JSON files in the `config/database_configs/` directory and running the script with the respective configuration name.

By following these steps, you should be able to automate the creation of databases and tasks in Notion efficiently.