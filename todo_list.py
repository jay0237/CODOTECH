import json
import os

def display_menu():
    print("\n--- To-Do List Menu ---")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Edit Task")
    print("4. Delete Task")
    print("5. Sort Tasks")
    print("6. Mark Task as Completed")  # New option
    print("7. Exit")                    # Exit is now option 7

def load_tasks(filename="tasks.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks, filename="tasks.json"):
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)

def view_tasks(tasks):
    print("\n--- Your Tasks ---")
    if not tasks:
        print("No tasks available.")
    else:
        for i, task in enumerate(tasks, start=1):
            status = "✓" if task.get('completed', False) else "✗"
            print(f"{i}. [{status}] {task['name']} (Priority: {task['priority']})")

def add_task(tasks):
    name = input("Enter the task name: ").strip()
    if not name:
        print("Task cannot be empty.")
        return
    priority = input("Enter priority (High/Medium/Low): ").capitalize()
    if priority not in ['High', 'Medium', 'Low']:
        print("Invalid priority. Setting to 'Low'.")
        priority = 'Low'
    task = {'name': name, 'priority': priority, 'completed': False}
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{name}' with priority '{priority}' added.")

def edit_task(tasks):
    if not tasks:
        print("No tasks to edit.")
        return

    view_tasks(tasks)
    try:
        index = int(input("Enter the task number to edit: ")) - 1
        if 0 <= index < len(tasks):
            new_name = input("Enter the new task name: ").strip()
            if not new_name:
                print("Task name cannot be empty.")
                return
            new_priority = input("Enter new priority (High/Medium/Low): ").capitalize()
            if new_priority not in ['High', 'Medium', 'Low']:
                print("Invalid priority. Keeping previous priority.")
                new_priority = tasks[index]['priority']
            old_task = tasks[index]
            tasks[index] = {
                'name': new_name,
                'priority': new_priority,
                'completed': old_task.get('completed', False)
            }
            save_tasks(tasks)
            print(f"Task '{old_task['name']}' updated to '{new_name}' with priority '{new_priority}'.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def delete_task(tasks):
    if not tasks:
        print("No tasks to delete.")
        return

    view_tasks(tasks)
    try:
        index = int(input("Enter the task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            print(f"Task '{removed['name']}' deleted.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def sort_tasks(tasks):
    if not tasks:
        print("No tasks to sort.")
        return

    print("\nSort by:")
    print("1. Name (A–Z)")
    print("2. Priority (High → Low)")
    choice = input("Enter choice (1/2): ")

    if choice == '1':
        tasks.sort(key=lambda x: x['name'].lower())
        save_tasks(tasks)
        print("Tasks sorted by name.")
    elif choice == '2':
        priority_order = {'High': 1, 'Medium': 2, 'Low': 3}
        tasks.sort(key=lambda x: priority_order.get(x['priority'], 4))
        save_tasks(tasks)
        print("Tasks sorted by priority.")
    else:
        print("Invalid choice.")

def mark_task_completed(tasks):
    if not tasks:
        print("No tasks to mark as completed.")
        return

    view_tasks(tasks)
    try:
        index = int(input("Enter the task number to mark as completed: ")) - 1
        if 0 <= index < len(tasks):
            if tasks[index].get('completed', False):
                print(f"Task '{tasks[index]['name']}' is already completed.")
            else:
                tasks[index]['completed'] = True
                save_tasks(tasks)
                print(f"Task '{tasks[index]['name']}' marked as completed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    tasks = load_tasks()

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            edit_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            sort_tasks(tasks)
        elif choice == '6':
            mark_task_completed(tasks)
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
