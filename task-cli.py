import time 
import sys
import json
import os 
from typing import List 

class Task: 
    _id_counter = 0

    def __init__(self, description, id=None, status="todo", created_at=None, update_at=None): 
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at if created_at is not None else self.get_timestamp()
        self.update_at = update_at if update_at is not None else self.get_timestamp()

    def to_dict(self): 
        return {
            "id": self.id, 
            "description": self.description, 
            "status": self.status,
            "created_at": self.created_at, 
            "update_at": self.update_at
        }
    
    @classmethod
    def set_id_counter(cls, value): 
        cls._id_counter = value 
    
    @classmethod
    def get_next_id(cls): 
        cls._id_counter += 1
        return cls._id_counter
    
    @staticmethod
    def get_timestamp(): 
        return time.ctime()

class Storage: 
    def __init__(self): 
        self.filename = "tasks_database.json"
        self.tasks: List[Task] = [] 

        if os.path.exists(self.filename): 
            if os.path.getsize(self.filename) > 0: 
                try:
                    with open(self.filename, "r", encoding="utf-8") as file:
                        raw_data = json.load(file)

                    self.tasks = [Task(**d) for d in raw_data]

                    if raw_data:
                        Task.set_id_counter(max(d['id'] for d in raw_data))
                except json.JSONDecodeError: 
                    print("Error: Database file is corrupted. Starting with an empty list.")
                    self.tasks = []
            else:
                self.tasks = []
        else: 
            self.tasks = []

    def store_data(self): 
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4, ensure_ascii=False)


class CLI:    
    def __init__(self): 
        self.storage = Storage()

    def show_instructions(self):
        print("\nWelcome to the Task Tracker CLI!")
        print("- To show all tasks use command: {list}")
        print("- To show completed tasks use command: {list done}")
        print("- To show tasks in progress use command: {list in-progress}")
        print("- To add a task use command: {add \"description\"}")
        print("- To update a task use command: {update [id] \"new description\"}")
        print("- To delete a task use command: {delete [id]}")
        print("- To mark task in progress use command: {mark-in-progress [id]}")
        print("- To mark task as done use command: {mark-done [id]}") 

    def add_task(self, description):
        new_id = Task.get_next_id()
        task = Task(description, new_id)
        self.storage.tasks.append(task)
        self.storage.store_data()
        print(f"Task added successfully (ID: {new_id}).")

    def update_task(self, id, new_description): 
        for task in self.storage.tasks: 
            if task.id == id: 
                task.description = new_description
                task.update_at = Task.get_timestamp()
                print(f"Task {id} updated successfully.")
                self.storage.store_data()
                return 
        print(f"Error: Task with ID {id} not found.")

    def delete_task(self, id): 
        for task in self.storage.tasks: 
            if task.id == id: 
                self.storage.tasks.remove(task)
                print(f"Task {id} deleted successfully.")
                self.storage.store_data()
                return 
        print(f"Error: Task with ID {id} not found.")
    
    def change_status(self, id, new_status): 
        for task in self.storage.tasks: 
            if task.id == id: 
                task.status = new_status
                task.update_at = Task.get_timestamp()
                print(f"Status for task {id} changed to '{new_status}'.")
                self.storage.store_data()
                return 
        print(f"Error: Task with ID {id} not found.")
    
    def show_tasks(self): 
        if not self.storage.tasks: 
            print("No tasks found.")
            return 
        
        print("\nAll Tasks:") 
        for task in self.storage.tasks: 
            print(f"• {task.id}: {task.description} [{task.status}] (Created: {task.created_at})")

    def show_tasks_by_filter(self, status_filter): 
        filtered_tasks = [t for t in self.storage.tasks if t.status == status_filter]
        
        if not filtered_tasks: 
            print(f"No tasks with status '{status_filter}' found.")
            return 
        
        print(f"\nTasks with status '{status_filter}':") 
        for task in filtered_tasks:
            print(f"• {task.id}: {task.description} [{task.status}] (Created: {task.created_at})")

def main(): 
    if len(sys.argv) < 2: 
        print("Usage: python task_tracker.py <command> [arguments]")
        print("Type 'python task_tracker.py --help' for details.")
        return 

    app = CLI()
    command = sys.argv[1]

    status_map = {
        "mark-in-progress": "in-progress",
        "mark-done": "done",
        "mark-todo": "todo"
    }

    match command:
        case "--help":
            app.show_instructions()
        case "add": 
            if len(sys.argv) < 3: 
                print("Error: Missing description.")
            else: 
                description = sys.argv[2]
                app.add_task(description)
        case "update": 
            if len(sys.argv) < 4: 
                print("Error: Usage: update [id] [description]")
            else: 
                try: 
                    task_id = int(sys.argv[2])
                    description = ' '.join(sys.argv[3:])
                    app.update_task(task_id, description)
                except ValueError: 
                    print("Error: ID must be a number.")                
        case "delete": 
            if len(sys.argv) < 3: 
                print("Error: Usage: delete [id]")
            else: 
                try: 
                    task_id = int(sys.argv[2])
                    app.delete_task(task_id)
                except ValueError: 
                    print("Error: ID must be a number.")
        case "mark-in-progress" | "mark-done": 
            if len(sys.argv) < 3: 
                print("Error: Usage: mark-status [id]")
            else: 
                try: 
                    task_id = int(sys.argv[2])
                    new_status = status_map[command]
                    app.change_status(task_id, new_status)
                except ValueError: 
                    print("Error: ID must be a number.")
        case "list":
            if len(sys.argv) > 2:
                if sys.argv[2] == "tasks":
                    app.show_tasks()
                else:
                    app.show_tasks_by_filter(sys.argv[2])
            else: 
                app.show_tasks()
        case _:
            print(f"Unknown command: {command}")

if __name__ == "__main__": 
    main()