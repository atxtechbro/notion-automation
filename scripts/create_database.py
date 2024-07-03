import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_PAGE_ID = os.getenv('NOTION_PAGE_ID')  # The ID of the Notion page where the database will be created

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

def create_database():
    create_url = 'https://api.notion.com/v1/databases'

    data = {
        "parent": {"type": "page_id", "page_id": NOTION_PAGE_ID},
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "Tasks Database"
                }
            }
        ],
        "properties": {
            "Name": {
                "title": {}
            },
            "Description": {
                "rich_text": {}
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Not Started", "color": "red"},
                        {"name": "In Progress", "color": "yellow"},
                        {"name": "Completed", "color": "green"}
                    ]
                }
            },
            "Due Date": {
                "date": {}
            }
        }
    }

    response = requests.post(create_url, headers=headers, json=data)

    if response.status_code == 200:
        database_id = response.json()["id"]
        print(f"Database created successfully with ID: {database_id}")
        return database_id
    else:
        print(f"Failed to create database: {response.text}")
        return None

def create_task(database_id, task):
    create_url = 'https://api.notion.com/v1/pages'

    data = {
        "parent": {"database_id": database_id},
        "properties": task["properties"]
    }

    response = requests.post(create_url, headers=headers, json=data)

    if response.status_code == 200:
        task_name = task["properties"]["Name"]["title"][0]["text"]["content"]
        print(f"Task '{task_name}' created successfully.")
    else:
        print(f"Failed to create task: {response.text}")

def main():
    if NOTION_PAGE_ID is None or NOTION_PAGE_ID == '':
        print("Error: NOTION_PAGE_ID is not set or is empty. Please set it in the .env file.")
        return

    database_id = create_database()
    if database_id:
        with open('config/tasks.json', 'r') as f:
            tasks = json.load(f)
        
        for task in tasks:
            create_task(database_id, task)

if __name__ == "__main__":
    main()
