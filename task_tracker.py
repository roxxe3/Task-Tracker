import json
import uuid
import datetime


class Task:
    def __init__(self, description, status):
        self.id = uuid.uuid4()
        self.description= description
        self.status = status
        self.createdAt= datetime.datetime.now()
        self.updatedAt= datetime.datetime.now()
    
    def add_task(self):
        
        task_data = {
            "id": f"{self.id}",
            "description": self.description,
            "status": self.status,
            "createdAt": f"{self.createdAt}",
            "updatedAt": f"{self.updatedAt}"
        }
        try:
            with open("data.json", 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []
        json_data.append(task_data)
        with open('data.json', 'w') as file:
            json.dump(json_data, file, indent=4)

    def update_task(id, description):
        try:
            with open("data.json", 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []
            
        task_found = False
        for task in json_data:
            if task["id"] == id:
                task["description"] = description
                task["updatedAt"] = str(datetime.datetime.now())
                task_found = True
                print("Task updated successfully")
                break
                
        if not task_found:
            print("Task not found")
            
        with open('data.json', 'w') as file:
            json.dump(json_data, file, indent=4)


    def delete_task(id):
        try:
            with open("data.json", 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []

        for task in range(len(json_data)):
            if json_data[task]["id"] == id:
                del json_data[task]
                print(f"Task Deleted ({id})")
            else:
                print("Task not found")
            with open('data.json', 'w') as file:
                json.dump(json_data, file, indent=4)

    def mark_in_progress(status, id):

        stat = ""
        if status == "mark-in-progress":
            stat = "in progress"
        if status == "mark-done":
            stat = "done"
            
        try:
            with open("data.json", 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []
        for task in json_data:
            if task["id"] == id:
                task["status"] = stat
            with open('data.json', 'w') as file:
                json.dump(json_data, file, indent=4)
            print("updated status")
    
    def list_tasks(status=None):
        try:
            with open("data.json", 'r') as file:
                json_data = json.load(file)
        except:
            json_data = []
        print(status)
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
            task = input('task-cli > ')  # Better prompt formatting
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
                
                case "mark-in-progress" | "mark-done":
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
                
                case _:
                    print("Command not found. Type 'help' for available commands.")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
