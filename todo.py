# todo_list_gui_sqlite.py

import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_FILE = 'todo_gui.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_task():
    title = entry.get().strip()
    if title:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        conn.commit()
        conn.close()
        entry.delete(0, tk.END)
        refresh_tasks()
    else:
        messagebox.showwarning("Warning", "Task title cannot be empty.")

def refresh_tasks():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, title, done FROM tasks")
    tasks = c.fetchall()
    conn.close()

    for task in tasks:
        status = "✓" if task[2] else "✗"
        listbox.insert(tk.END, f"{task[0]}. [{status}] {task[1]}")

def toggle_done():
    selected = listbox.curselection()
    if selected:
        text = listbox.get(selected[0])
        task_id = int(text.split('.')[0])
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # toggle: if done=1 -> set to 0, else set to 1
        c.execute("UPDATE tasks SET done = CASE done WHEN 1 THEN 0 ELSE 1 END WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        refresh_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected.")

def delete_task():
    selected = listbox.curselection()
    if selected:
        text = listbox.get(selected[0])
        task_id = int(text.split('.')[0])
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        refresh_tasks()
    else:
        messagebox.showwarning("Warning", "No task selected.")

# Initialize DB
init_db()

# GUI setup
root = tk.Tk()
root.title("To-Do List (SQLite)")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=40)
entry.grid(row=0, column=0, padx=5, pady=5)

add_btn = tk.Button(frame, text="Add Task", command=add_task)
add_btn.grid(row=0, column=1, padx=5, pady=5)

listbox = tk.Listbox(frame, width=50)
listbox.grid(row=1, column=0, columnspan=2, pady=5)

toggle_btn = tk.Button(frame, text="Toggle Complete", command=toggle_done)
toggle_btn.grid(row=2, column=0, pady=5)

delete_btn = tk.Button(frame, text="Delete Task", command=delete_task)
delete_btn.grid(row=2, column=1, pady=5)

refresh_tasks()

root.mainloop()
