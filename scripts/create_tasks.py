import json
import os
import requests

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

def create_task(task):
    create_url = 'https://api.notion.com/v1/pages'
    
    data = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": task['name']
                        }
                    }
                ]
            },
            "Description": {
                "rich_text": [
                    {
                        "text": {
                            "content": task['description']
                        }
                    }
                ]
            }
        }
    }
    
    response = requests.post(create_url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"Task '{task['name']}' created successfully.")
    else:
        print(f"Failed to create task '{task['name']}': {response.text}")

def main():
    with open('config/tasks.json', 'r') as f:
        tasks = json.load(f)
        
    for task in tasks:
        create_task(task)

if __name__ == "__main__":
    main()
