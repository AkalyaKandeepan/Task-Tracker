import json
import shlex
from datetime import datetime
import sys

FILE_NAME = "../Task-Tracker/task.json"


# ---------- Utility Functions ----------

def load_tasks():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=2)


def find_task_index(tasks, task_id):
    for index, task in enumerate(tasks):
        if task["id"] == int(task_id):
            return index
    return -1


def get_current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# ---------- Task Operations ----------

def add_task(command):
    if len(command) < 2:
        print("Error: Description required for 'add'")
        return

    tasks = load_tasks()
    new_id = tasks[-1]['id'] + 1 if tasks else 1
    now = get_current_time()

    new_task = {
        "id": new_id,
        "description": command[1],
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added successfully (ID: {new_id})")


def update_task(command):
    if len(command) < 3:
        print("Error: Task ID and new description required for 'update'")
        return

    tasks = load_tasks()
    index = find_task_index(tasks, command[1])

    if index == -1:
        print(f"❌ Task with ID {command[1]} not found.")
        return

    tasks[index]["description"] = command[2]
    tasks[index]["updatedAt"] = get_current_time()
    save_tasks(tasks)

    print(f"✅ Task updated (ID: {command[1]})")


def delete_task(command):
    if len(command) < 2:
        print("Error: Task ID required for 'delete'")
        return

    tasks = load_tasks()
    index = find_task_index(tasks, command[1])

    if index == -1:
        print(f"❌ Task with ID {command[1]} not found.")
        return

    deleted = tasks.pop(index)
    save_tasks(tasks)
    print(f"🗑️ Deleted task (ID: {deleted['id']})")


def change_status(command, status):
    if len(command) < 2:
        print(f"Error: Task ID required for '{command[0]}'")
        return

    tasks = load_tasks()
    index = find_task_index(tasks, command[1])

    if index == -1:
        print(f"❌ Task with ID {command[1]} not found.")
        return

    tasks[index]["status"] = status
    tasks[index]["updatedAt"] = get_current_time()
    save_tasks(tasks)

    print(f"✅ Task status updated to '{status}' (ID: {command[1]})")


def list_tasks(command):
    tasks = load_tasks()

    if len(command) == 1:
        for task in tasks:
            print_task(task)
    else:
        status_filter = command[1]
        filtered = [task for task in tasks if task["status"] == status_filter]
        for task in filtered:
            print_task(task)


def print_task(task):
    print(f"[{task['id']}] {task['description']} - {task['status']} (Updated: {task['updatedAt']})")


# ---------- CLI Main Loop ----------

def main():
    print("📝 Task Tracker CLI (type 'exit' to quit)")
    print("Available commands: add, update, delete, mark-in-progress, mark-done, list")

    try:
        args = sys.argv[1:]

        if len(args) == 0:
            print("Error: Task ID and new description required for 'update'")
            raise SystemExit("Usage: python tasktracker.py command")

        command = args
        if not command:
            return

        action = command[0].lower()

        if action == "add":
            add_task(command)
        elif action == "update":
            update_task(command)
        elif action == "delete":
            delete_task(command)
        elif action == "mark-in-progress":
            change_status(command, "in-progress")
        elif action == "mark-done":
            change_status(command, "done")
        elif action == "list":
            list_tasks(command)
        elif action == "exit" or action == "quit":
            print("Exited.")
        else:
            print(f"❓ Unknown command: {action}")
            print("Available commands: add, update, delete, mark-in-progress, mark-done, list")

    except KeyboardInterrupt:
        print("\nExited.")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
