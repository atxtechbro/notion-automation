import argparse
from notion_utils.NotionUtils import load_schema, load_tasks, update_database, create_task

def main(database_id, schema_name, tasks_name):
    try:
        # Load schema and tasks configuration
        schema = load_schema(schema_name)
        tasks = load_tasks(tasks_name)

        # Update the database with the provided schema
        update_database(database_id, schema)

        # Add tasks to the updated database
        schema_properties = schema["properties"]
        for task in tasks["tasks"]:
            create_task(database_id, task, schema_properties)

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"Validation Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update an existing Notion database using specified schema and tasks templates.")
    parser.add_argument('database_id', type=str, help="The ID of the database to update.")
    parser.add_argument('schema', type=str, help="The name of the schema template to use (without .json extension).")
    parser.add_argument('tasks', type=str, help="The name of the tasks template to use (without .json extension).")
    
    args = parser.parse_args()
    main(args.database_id, args.schema, args.tasks)
