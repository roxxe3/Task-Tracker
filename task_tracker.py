import json
import uuid
import datetime


class Task:
    def __init__(self, description, status, file_name="data.json"):
        self.id = uuid.uuid4()
        self.description= description
        self.status = status
        self.createdAt= datetime.datetime.now()
        self.updatedAt= datetime.datetime.now()
        self.file_name = file_name
    
    def add_task(self):
        
        task_data = {
            "id": f"{self.id}",
            "description": self.description,
            "status": self.status,
            "createdAt": f"{self.createdAt}",
            "updatedAt": f"{self.updatedAt}"
        }
        try:
            with open(self.file_name, 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []
        json_data.append(task_data)
        with open(self.file_name, 'w') as file:
            json.dump(json_data, file, indent=4)

    @staticmethod
    def update_task(task_id, new_description, file_name="data.json"):
        try:
            with open(file_name, "r") as file:
                json_data = json.load(file)
        except:
            json_data = []

        for task in json_data:
            if task["id"] == task_id:
                task["description"] = new_description
                task["updatedAt"] = str(datetime.datetime.now())
                break
        with open(file_name, "w") as file:
            json.dump(json_data, file, indent=4)


    def delete_task(id, file_name="data.json"):
        try:
            with open(file_name, 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []

        for task in range(len(json_data)):
            if json_data[task]["id"] == id:
                del json_data[task]
                print(f"Task Deleted ({id})")
            else:
                print("Task not found")
            with open(file_name, 'w') as file:
                json.dump(json_data, file, indent=4)

    @staticmethod
    def mark_in_progress(task_id, file_name="data.json"):
        try:
            with open(file_name, "r") as file:
                json_data = json.load(file)
        except:
            json_data = []

        task_found = False
        for task in json_data:
            if task["id"] == task_id:
                task["status"] = "in progress"
                task["updatedAt"] = str(datetime.datetime.now())
                task_found = True
                break
        
        if not task_found:
            print("task not found")
            
        with open(file_name, "w") as file:
            json.dump(json_data, file, indent=4)
    
    def list_tasks(status=None, file_name="data.json"):
        if status == "in-progress":
            status = "in progress"
        try:
            with open(file_name, 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []
        if not json_data:
            print("No tasks found")
            return
        
        if status != None:
            for task in json_data:
                if task["status"] == status:
                    print(task["description"])
        else:
            for task in json_data:
                print(task["description"])


def input_parse_command(input):
    splited= input.split(" ")
    if len(splited) > 1:
        return [splited[0], splited[1]]
    return splited

def input_parse_description(input_str):
    # Split the input by spaces
    parts = input_str.split('"')
    
    if len(parts) > 1:
        # If there is a quoted part, it's between parts[1] (quotes removed)
        return parts[1]
    else:
        # Otherwise, return the whole input, stripped of spaces
        return input_str.strip()




if __name__ == "__main__":
    COMMANDS = {
        "add": "Add a new task",
        "update": "Update an existing task",
        "mark-in-progress": "Mark task as in progress",
        "mark-done": "Mark task as completed",
        "delete": "Delete a task",
        "list": "List all tasks",
        "help": "Show this help message",
        "exit": "Exit the program"
    }

    while True:
        try:
            task = input('task-cli > ')
            if task.lower() == 'exit':
                print("Goodbye!")
                break

            parse = input_parse_command(task)
            if not parse:
                print("Invalid command. Type 'help' for available commands.")
                continue

            command = parse[0].lower()
            id = parse[1] if len(parse) > 1 else ""
            description = input_parse_description(task.replace(command, ''))

            match command:  # Using match statement for better readability
                case "add":
                    new_task = Task(description, "in progress")
                    new_task.add_task()
                    print(f"Task added successfully (ID: {new_task.id})")
                
                case "update":
                    if not id:
                        print("Error: Task ID required for update")
                        continue
                    Task.update_task(id, description)
                
                case "mark-in-progress" | "mark-done" | "todo":
                    if not id:
                        print("Error: Task ID required for marking status")
                        continue
                    Task.mark_in_progress(command, id)
                
                case "delete":
                    if not id:
                        print("Error: Task ID required for deletion")
                        continue
                    Task.delete_task(id)
                
                case "help":
                    print("\nAvailable commands:")
                    for cmd, desc in COMMANDS.items():
                        print(f"  {cmd:<15} - {desc}")
                
                case "list":
                    Task.list_tasks(id)
                    continue
                
                case _:
                    print("Command not found. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
            
