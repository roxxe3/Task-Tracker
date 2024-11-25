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
        for task in json_data:
            if task["id"] == id:
                task["description"] = description
            with open('data.json', 'w') as file:
                json.dump(json_data, file, indent=4)
            print("updated")
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



def input_parse_command(input):
    splited= input.split(" ")
    print(splited)
    return [splited[0], splited[1]]

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
    while(True):
        task = input('task-cli ')
        parse = input_parse_command(task)
        command, id = parse[0],parse[1]
        description = input_parse_description(task.replace(command, ''))
        if command == "add":
            new_task = Task(description, "in progress")
            new_task.add_task()
            print(f"Task added successfully (ID: {new_task.id})")
        if command == "update":
            Task.update_task(id, description)
        if command == "mark-in-progress" or command == "mark-done":
            Task.mark_in_progress(command, id)

