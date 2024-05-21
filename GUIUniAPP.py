import tkinter as tk
from tkinter import messagebox
import pickle
import os
import random
import tkinter.simpledialog

class Subject:
    def __init__(self):
        self.id = self.generate_id()
        self.score = random.randint(25, 100)
        self.grade = self.determine_grade()

    def generate_id(self):
        return str(random.randint(1, 999)).zfill(3)

    def determine_grade(self):
        if self.score < 50:
            return 'Z'
        elif 50 <= self.score < 65:
            return 'P'
        elif 65 <= self.score < 75:
            return 'C'
        elif 75 <= self.score < 85:
            return 'D'
        elif self.score >= 85:
            return 'HD'

    def __str__(self):
        return f"Subject ID: {self.id}, Score: {self.score}, Grade: {self.grade}"

class Student:
    def __init__(self, name, email, password):
        self.id = str(random.randint(1, 999999)).zfill(6)
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

class Database:
    def __init__(self, filename='students.data'):
        self.filename = filename
        self.check_file_exists()

    def check_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'wb') as file:
                pickle.dump([], file)

    def read_students(self):
        self.check_file_exists()
        with open(self.filename, 'rb') as file:
            return pickle.load(file)

    def update_student(self, student):
        students = self.read_students()
        updated_students = [s for s in students if s.id != student.id]
        updated_students.append(student)
        with open(self.filename, 'wb') as file:
            pickle.dump(updated_students, file)


class StudentInfoWindow:
    def __init__(self, root, student):
        self.root = root
        self.student = student
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Student Dashboard")
        self.main_frame = tk.Frame(self.root, bg='lightgrey', pady=20, padx=20)
        self.main_frame.pack(padx=10, pady=10)

        tk.Label(self.main_frame, text=f"Welcome {self.student.name}", bg='lightgrey').pack(anchor='w', pady=10)
        tk.Label(self.main_frame, text=f"Email: {self.student.email}", bg='lightgrey').pack(anchor='w', pady=5)
        tk.Label(self.main_frame, text=f"Student ID: {self.student.id}", bg='lightgrey').pack(anchor='w', pady=5)

        tk.Button(self.main_frame, text="Register New Subject", command=self.register_subject).pack(pady=5)
        tk.Button(self.main_frame, text="View Subjects", command=self.view_subjects).pack(pady=5)
        tk.Button(self.main_frame, text="Remove Subject", command=self.remove_subject).pack(pady=5)
        tk.Button(self.main_frame, text="Logout", command=self.logout).pack(pady=10)

    def register_subject(self):
        if len(self.student.subjects) >= 4:
            messagebox.showerror("Registration Failed", "You cannot register more than 4 subjects.")
            return
        new_subject = Subject()
        self.student.subjects.append(new_subject)
        messagebox.showinfo("Registration Successful", f"Registered new subject: {new_subject}")
        self.update_student()

    def view_subjects(self):
        subjects_info = "\n".join(str(subject) for subject in self.student.subjects)
        messagebox.showinfo("Registered Subjects", subjects_info if subjects_info else "No subjects registered.")

    def remove_subject(self):
        if not self.student.subjects:
            messagebox.showerror("Error", "No subjects to remove.")
            return

        subjects_str = "\n".join(f"ID: {subject.id}, {subject}" for subject in self.student.subjects)
        subject_id = tk.simpledialog.askstring("Remove Subject",
                                               f"Enter the ID of the subject you want to remove:\n{subjects_str}")

        if subject_id is None:  
            messagebox.showinfo("Cancelled", "Subject removal cancelled.")
            return

        subject_to_remove = None
        for subject in self.student.subjects:
            if subject.id == subject_id:
                subject_to_remove = subject
                break

        if subject_to_remove:
            self.student.subjects.remove(subject_to_remove)
            self.update_student()
            messagebox.showinfo("Success", "Subject removed successfully.")
        else:
            messagebox.showerror("Error", "No subject found with ID: " + subject_id)

    def logout(self):
        self.main_frame.pack_forget()
        LoginWindow(self.root)

    def update_student(self):
        self.db = Database()
        self.db.update_student(self.student)


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("GUIUniApp")
        self.main_frame = tk.Frame(self.root, bg='lightgrey', pady=20, padx=20)
        self.main_frame.pack(padx=10, pady=10)

        tk.Label(self.main_frame, text="Email:", bg='lightgrey').pack(anchor='w')
        self.email_entry = tk.Entry(self.main_frame, width=30)
        self.email_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Password:", bg='lightgrey').pack(anchor='w')
        self.password_entry = tk.Entry(self.main_frame, show='*', width=30)
        self.password_entry.pack(pady=5)

        self.status_label = tk.Label(self.main_frame, text="", bg='lightgrey', fg='red')
        self.status_label.pack(pady=5)

        tk.Button(self.main_frame, text="Login", command=self.login).pack(pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        students = self.db.read_students()
        for student in students:
            if student.email == email and student.password == password:
                self.status_label.config(text=f"Welcome {student.name}!", fg='green')
                self.main_frame.pack_forget()  # 清除登录窗口
                StudentInfoWindow(self.root, student)  # 跳转到学生信息窗口
                return
        self.status_label.config(text="Incorrect email or password.", fg='red')



def main():
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
