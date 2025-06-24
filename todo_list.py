import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

FILENAME = "tasks.json"

def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        json.dump(tasks, file, indent=4)


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = load_tasks()

        # Treeview with 3 columns: Task, Priority, Status
        self.tree = ttk.Treeview(root, columns=("Task", "Priority", "Status"), show="headings", height=10)
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Completed")

        self.tree.column("Task", width=250)
        self.tree.column("Priority", width=100, anchor="center")
        self.tree.column("Status", width=80, anchor="center")
        self.tree.pack(pady=10, fill="x")

        self.update_task_list()

        # Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Edit Task", command=self.edit_task).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Mark Completed", command=self.mark_completed).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Sort Tasks", command=self.sort_tasks).grid(row=0, column=4, padx=5)

    def update_task_list(self):
        self.tree.delete(*self.tree.get_children())
        for i, task in enumerate(self.tasks):
            status = "✓" if task.get("completed", False) else "✗"
            self.tree.insert("", "end", iid=i, values=(task["name"], task["priority"], status))

    def add_task(self):
        name = simpledialog.askstring("Task Name", "Enter task name:")
        if not name:
            return
        priority = simpledialog.askstring("Priority", "Enter priority (High/Medium/Low):", initialvalue="Low")
        if priority not in ["High", "Medium", "Low"]:
            priority = "Low"
        self.tasks.append({"name": name, "priority": priority, "completed": False})
        save_tasks(self.tasks)
        self.update_task_list()

    def edit_task(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to edit.")
            return
        task = self.tasks[int(selected)]
        new_name = simpledialog.askstring("Edit Task", "Enter new task name:", initialvalue=task["name"])
        if not new_name:
            return
        new_priority = simpledialog.askstring("Edit Priority", "Enter new priority (High/Medium/Low):", initialvalue=task["priority"])
        if new_priority not in ["High", "Medium", "Low"]:
            new_priority = task["priority"]
        task["name"] = new_name
        task["priority"] = new_priority
        save_tasks(self.tasks)
        self.update_task_list()

    def delete_task(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to delete.")
            return
        del self.tasks[int(selected)]
        save_tasks(self.tasks)
        self.update_task_list()

    def mark_completed(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a task to mark as completed.")
            return
        self.tasks[int(selected)]["completed"] = True
        save_tasks(self.tasks)
        self.update_task_list()

    def sort_tasks(self):
        sort_option = simpledialog.askstring("Sort Tasks", "Sort by:\n1. Name\n2. Priority", initialvalue="1")
        if sort_option == "1":
            self.tasks.sort(key=lambda x: x["name"].lower())
        elif sort_option == "2":
            order = {"High": 1, "Medium": 2, "Low": 3}
            self.tasks.sort(key=lambda x: order.get(x["priority"], 4))
        else:
            messagebox.showinfo("Invalid", "Invalid sort option.")
            return
        save_tasks(self.tasks)
        self.update_task_list()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
