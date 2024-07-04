import json
import os

def add_task_from_raw(file_path='config/tasks.json', raw_task_dir='config'):
    """Adds a new task from a raw JSON file to the tasks.json file."""
    raw_task_path = os.path.join(raw_task_dir, 'new_task_raw.json')
    
    # Check if the raw task file exists
    if not os.path.exists(raw_task_path):
        print("No new raw task file found.")
        return
    
    # Load the new task from the raw JSON file
    with open(raw_task_path, 'r') as file:
        task = json.load(file)
    
    # Initialize tasks list
    tasks = []

    # Load existing tasks from tasks.json if it exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                tasks = json.load(file)
            except json.JSONDecodeError:
                # Handle the case where tasks.json is empty or contains invalid JSON
                tasks = []

    # Add the new task to the list of tasks
    tasks.append(task)
    
    # Save the updated tasks back to tasks.json
    with open(file_path, 'w') as file:
        json.dump(tasks, file, indent=4)
    
    # Optionally, delete or archive the raw task file
    os.remove(raw_task_path)  # To delete
    # shutil.move(raw_task_path, 'path/to/archive')  # To archive

# Example usage
# This function would be called without the task parameter, relying on the presence of new_task_raw.json
add_task_from_raw()
