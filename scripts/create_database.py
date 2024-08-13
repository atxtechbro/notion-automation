import argparse
from notion_utils.NotionUtils import load_schema, load_tasks, create_database, create_task

def main(schema_name, tasks_name):
    try:
        schema = load_schema(schema_name)  # Load schema configuration
        tasks = load_tasks(tasks_name)  # Load tasks configuration

        database_id = create_database(schema)
        if database_id:
            schema_properties = schema["properties"]
            for task in tasks["tasks"]:
                create_task(database_id, task, schema_properties)
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"Validation Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Notion database using a specified schema and tasks template.")
    parser.add_argument('schema', type=str, help="The name of the schema template to use (without .json extension).")
    parser.add_argument('tasks', type=str, help="The name of the tasks template to use (without .json extension).")
    
    args = parser.parse_args()
    main(args.schema, args.tasks)
