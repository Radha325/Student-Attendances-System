import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime


conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
''')
conn.commit()

def add_student():
    name = entry_name.get()
    if name:
        cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
        entry_name.delete(0, END)
        refresh_student_list()
    else:
        messagebox.showwarning("Input Error", "Please enter student name")

def mark_attendance():
    selected_student = student_combo.get()
    status = status_combo.get()
    if selected_student and status:
        cursor.execute("SELECT id FROM students WHERE name = ?", (selected_student,))
        student_id = cursor.fetchone()[0]
        date_today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (student_id, date_today))
        if cursor.fetchone():
            messagebox.showinfo("Already marked", "Attendance already marked for today")
        else:
            cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                           (student_id, date_today, status))
            conn.commit()
            messagebox.showinfo("Success", "Attendance marked")
    else:
        messagebox.showwarning("Selection Error", "Please select student and status")

def refresh_student_list():
    cursor.execute("SELECT name FROM students")
    students = [row[0] for row in cursor.fetchall()]
    student_combo['values'] = students

def show_attendance():
    tree.delete(*tree.get_children())
    cursor.execute('''
        SELECT students.name, attendance.date, attendance.status 
        FROM attendance 
        JOIN students ON attendance.student_id = students.id
        ORDER BY attendance.date DESC
    ''')
    rows = cursor.fetchall()
    for row in rows:
        tree.insert('', END, values=row)


root = Tk()
root.title("Student Attendance System")
root.geometry("700x600")
root.configure(bg="#f0f0f0")

title = Label(root, text="Student Attendance System", font=("Arial", 20, "bold"), bg="#f0f0f0")
title.pack(pady=10)


frame_add = Frame(root, bg="#f0f0f0")
frame_add.pack(pady=10)

Label(frame_add, text="Student Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
entry_name = Entry(frame_add, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=5)

btn_add = Button(frame_add, text="Add Student", command=add_student, bg="#4caf50", fg="white", width=20)
btn_add.grid(row=0, column=2, padx=10)


frame_attendance = Frame(root, bg="#f0f0f0")
frame_attendance.pack(pady=10)

Label(frame_attendance, text="Select Student:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
student_combo = ttk.Combobox(frame_attendance, width=27)
student_combo.grid(row=0, column=1, padx=10, pady=5)

Label(frame_attendance, text="Status:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=2, padx=10, pady=5)
status_combo = ttk.Combobox(frame_attendance, values=["Present", "Absent"], width=10)
status_combo.grid(row=0, column=3, padx=10, pady=5)

btn_mark = Button(frame_attendance, text="Mark Attendance", command=mark_attendance, bg="#2196f3", fg="white", width=20)
btn_mark.grid(row=0, column=4, padx=10)


frame_display = Frame(root, bg="#f0f0f0")
frame_display.pack(pady=10)

btn_show = Button(root, text="Show Attendance Records", command=show_attendance, bg="#ff9800", fg="white", width=30)
btn_show.pack(pady=10)

tree = ttk.Treeview(root, columns=("Name", "Date", "Status"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Date", text="Date")
tree.heading("Status", text="Status")
tree.pack(pady=10, fill=BOTH, expand=True)


refresh_student_list()

root.mainloop()