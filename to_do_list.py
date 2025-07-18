import tkinter as tk
from tkinter import messagebox
import sqlite3

database_file = 'todogui.db'

def initial_database():
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
            ) 
        ''')

    connection.commit()
    connection.close()

def task():
    title = entry.get().strip()
    if title:
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        connection.commit()
        connection.close()
        entry.deleted(0,tk.END)
        tasks_refresh()
    else:
        messagebox.showwarning("Warning", "Task title cannot be empty.")

def tasks_refresh():
    listbox.delete(0, tk.END)
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, done FROM tasks")
    tasks = cursor.fetchall()
    connection.close()

    for task in tasks:
        status = "✓" if task[2] else "✗"
        listbox.insert(tk.END, f"{task[0]}.[{status}] {task[1]}")

def toggle():
    selected = listbox.cursorselected()
    if selected:
        txt = listbox.get(selected[0])
        id_task = int(txt.split('.')[0])
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()

        cursor.execute("UPDATE tasks SET done = CASE done wHEN 1 THEN 0 ELSE 1 END WHERE id=?", (id_task,))
        connection.commit()
        connection.close()
        tasks_refresh()
    else:
        messagebox.showwarning("Warnong", "No task selected.")

def deletedtask():
    selected = listbox.cursorselection()
    if selected:
        txt = listbox.get(selected[0])
        id_task = int(txt.split('.')[0])
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (id_task,))
        connection.commit()
        connection.close()
        tasks_refresh
    else:
        messagebox.showwarning("Warning!" "No tasks selected.")

initial_database()

window = tk.Tk()
window.title("To-Do List")

frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

entry = tk.Entry(frame, width=40)
entry.grid(row=0, column=0, padx=5, pady=5)

add_btn = tk.Button(frame, text="Add Task", command=task)
add_btn.grid(row=0, column=1, padx=5, pady=5)

listbox = tk.Listbox(frame, width=50)
listbox.grid(row=1, column=0, columnspan=2, pady=5)

toggle_btn = tk.Button(frame, text="Toggle Complete", command=toggle)
toggle_btn.grid(row=2, column=0, pady=5)

delete_btn = tk.Button(frame, text="Delete Task", command=deletedtask)
delete_btn.grid(row=2, column=1, pady=5)

tasks_refresh()

window.mainloop()
