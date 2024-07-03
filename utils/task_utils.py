import json

def add_task(task, file_path='config/tasks.json'):
    """Adds a new task to the tasks.json file."""
    try:
        # Open the existing tasks file
        with open(file_path, 'r') as file:
            # Load existing tasks
            tasks = json.load(file)
        
        # Add the new task
        tasks.append(task)
        
        # Write the updated tasks back to the file
        with open(file_path, 'w') as file:
            json.dump(tasks, file, indent=4)
            
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error: JSON decoding error.")
