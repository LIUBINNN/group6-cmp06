import random

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
        self.id = self.generate_id()
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    def generate_id(self):
        return str(random.randint(1, 999999)).zfill(6)

    def register_subject(self):
        if len(self.subjects) < 4:
            new_subject = Subject()
            self.subjects.append(new_subject)
            print(f"Registered subject: {new_subject}")
        else:
            print(f"\033[31mStudent are allowed to enrol in 4 subjects only.\033[0m")

    def drop_subject(self, subject_id):
        original_length = len(self.subjects)
        self.subjects = [subject for subject in self.subjects if subject.id != subject_id]
        return len(self.subjects) < original_length

    def list_subjects(self):
        for subject in self.subjects:
            print(subject)

    def change_password(self, new_password):
        self.password = new_password

    def __str__(self):
        return f"Student ID: {self.id}, Name: {self.name}, Email: {self.email}, Subjects: {[str(subject) for subject in self.subjects]}"

import pickle
import os
import threading

class Database:
    def __init__(self, filename='students.data'):
        self.filename = filename
        self.lock = threading.Lock()
        self.check_file_exists()

    def initialize_file(self):
        self.lock.acquire()
        try:
            if not os.path.exists(self.filename):
                with open(self.filename, 'wb') as file:
                    pickle.dump([], file)  
        finally:
            self.lock.release()

    def check_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'wb') as file:
                pickle.dump([], file)

    def email_exists(self, email):
        try:
            self.check_file_exists()
            with open(self.filename, 'rb') as file:
                students = pickle.load(file)
                return any(student.email == email for student in students)
        except Exception as e:
            print(f"Error reading from file: {e}")
            return False

    def write_student(self, student):
        self.lock.acquire()  
        try:
            with open(self.filename, 'rb+') as file:
                students = pickle.load(file)
                students = [s for s in students if s.id != student.id]
                students.append(student)
                file.seek(0)
                file.truncate()
                pickle.dump(students, file)
        except Exception as e:
            print(f"Error writing to file: {e}")
        finally:
            self.lock.release()  


    def read_students(self):
        with self.lock: 
            try:
                with open(self.filename, 'rb') as file:
                    return pickle.load(file)
            except Exception as e:
                print(f"Error reading from file: {e}")
                return []  


    def delete_student(self, student_id):
        try:
            self.check_file_exists()
            with open(self.filename, 'rb+') as file:
                students = pickle.load(file)
                new_students = [student for student in students if student.id != student_id]
                if len(students) == len(new_students):
                    return False
                file.seek(0)
                file.truncate()
                pickle.dump(new_students, file)
                return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False

    def clear_students(self):
     confirm = input("Are you sure you want to clear all student data? Type 'yes' to confirm: ")
     if confirm.lower() == 'yes':
        self.lock.acquire()  
        try:
            with open(self.filename, 'wb') as file:
                pickle.dump([], file)  
            print("All student data has been successfully cleared.")
        except Exception as e:
            print(f"Error clearing student data: {e}")
        finally:
            self.lock.release() 
     else:
        print("Operation cancelled.")


def main_menu():
    print("\n\033[36mWelcome to CLIUniApp\033[0m")
    print("\033[36mEnter 'A' for Admin menu\033[0m")
    print("\033[36mEnter 'S' for Student menu\033[0m")
    print("\033[36mEnter 'X' to Exit\033[0m")
    choice = input("\033[36mYour choice: \033[0m").upper()
    return choice

def student_menu():
    print("\n\033[36mStudent Menu\033[0m")
    print("\033[36m(L) Login\033[0m")
    print("\033[36m(R) Register\033[0m")
    print("\033[36m(X) Exit\033[0m")
    choice = input("\033[36mYour choice: \033[0m").upper()
    return choice

def student_course_menu(student):
    print(f"\n\033[36mWelcome, {student.name}\033[0m")
    print("\033[36m(C) Change Password\033[0m")
    print("\033[36m(E) Enroll Subject\033[0m")
    print("\033[36m(R) Drop Subject\033[0m")
    print("\033[36m(S) Show Subjects\033[0m")
    print("\033[36m(X) Exit\033[0m")
    choice = input("\033[36mYour choice: \033[0m").upper()
    return choice

def admin_menu():
    print("\n\033[36mAdmin Menu\033[0m")
    print("\033[36m(C) Clear Database\033[0m")
    print("\033[36m(G) Group Students by Grade\033[0m")
    print("\033[36m(P) Partition Students by Pass/Fail\033[0m")
    print("\033[36m(R) Remove Student\033[0m")
    print("\033[36m(S) Show All Students\033[0m")
    print("\033[36m(X) Exit\033[0m")
    choice = input("\033[36mYour choice: \033[0m").upper()
    return choice

import re

def valid_email(email):
    return re.match(r'^[a-zA-Z0-9._]*[a-zA-Z0-9]+\.[a-zA-Z0-9]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}$', email) and email.endswith('@university.com')

def valid_password(password):
    return re.match(r'^[A-Z][a-zA-Z]{4,}[0-9]{3,}$', password)

def handle_student_registration(database):
    print("\n\033[32mRegister New Student\033[0m")
    name = input("Enter full name: ")
    email = input("Enter email (must end with @university.com): ")    
    if not valid_email(email):
        print("\033[31m3Invalid email format, please try again.\033[0m")
        return
    password = input("Enter password (Start with a capital letter, at least 5 letters followed by 3 or more digits): ")
    if not valid_password(password):
        print("\033[31mInvalid password format, please try again.\033[0m")
        return
    if database.email_exists(email):
        print(f"\033[31mA student {name} already exists.\033[0m")
        return

    student = Student(name, email, password)
    database.write_student(student)
    print("Registration successful!")

def handle_enroll_subject(student, database):
    if len(student.subjects) >= 4:
        print(f"\033[31mYou have already enrolled in 4 subjects.\033[0m")
        return
    student.register_subject()
    database.write_student(student)
    print("Subject enrolled successfully.")

def handle_drop_subject(student, database):
    if not student.subjects:
        print("No subjects registered to drop.")
        return

    student.list_subjects()
    subject_id = input("Enter subject ID to drop: ")
    if student.drop_subject(subject_id):
        database.write_student(student)
        print("Subject dropped successfully.")
    else:
        print(f"No subject found with ID: {subject_id}")

def handle_change_password(student, database):
    new_password = input("Enter new password: ")
    while not valid_password(new_password):
        new_password = input(f"\033[31mInvalid password, please try again:\033[0m ")

    confirm_password = input("Confirm new password: ")
    while confirm_password != new_password:
        print(f"\033[31mPasswords do not match - Try again.\033[0m")
        confirm_password = input("Confirm new password: ")

    student.change_password(new_password)
    database.write_student(student)
    print("Password changed successfully.")


def handle_show_subjects(student):
    if not student.subjects:
        print("No subjects registered.")
    else:
        student.list_subjects()

def handle_clear_database(database):
    confirm = input(f"\033[31mAre you sure you want to clear all student data? Type 'yes' to confirm:\033[0m")
    if confirm.lower() == 'yes':
        database.clear_students()
        print("Database cleared successfully.")
    else:
        print("Operation cancelled.")

def handle_group_students_by_grade(database):
    students = database.read_students()
    grade_groups = {'Z': {}, 'P': {}, 'C': {}, 'D': {}, 'HD': {}}

    for student in students:
        student_info = f"{student.name}: {student.id} --> Email: {student.email}"
        student_subjects_by_grade = {grade: [] for grade in grade_groups.keys()}

        for subject in student.subjects:
            subject_info = f"Subject ID: {subject.id}, Score: {subject.score}, Grade: {subject.grade}"
            if subject_info not in student_subjects_by_grade[subject.grade]:
                student_subjects_by_grade[subject.grade].append(subject_info)

        for grade, subjects in student_subjects_by_grade.items():
            if subjects:
                if student.id not in grade_groups[grade]:
                    grade_groups[grade][student.id] = {
                        "info": student_info,
                        "subjects": subjects
                    }
                else:
                    grade_groups[grade][student.id]["subjects"].extend(subjects)
                    grade_groups[grade][student.id]["subjects"] = list(set(grade_groups[grade][student.id]["subjects"]))

    for grade, students in grade_groups.items():
        print(f"\nStudents with Grade {grade}:")
        for student_details in students.values():
            subjects_str = ', '.join(student_details["subjects"])
            print(f"{student_details['info']}, Subjects: [{subjects_str}]")

def handle_partition_students_by_pass_fail(database):
    students = database.read_students()
    pass_students = {}
    fail_students = {}

    for student in students:
        student_info = f"Student ID: {student.id}, Name: {student.name}, Email: {student.email}"
        subjects_list = [f"Subject ID: {sub.id}, Score: {sub.score}, Grade: {sub.grade}" for sub in student.subjects]

        if student.subjects:
            average_score = sum(sub.score for sub in student.subjects) / len(student.subjects)
            if average_score >= 50:
                pass_students[student.id] = {
                    "info": student_info,
                    "subjects": subjects_list,
                    "Average Score": average_score
                }
            else:
                fail_students[student.id] = {
                    "info": student_info,
                    "subjects": subjects_list,
                    "Average Score": average_score
                }
        else:
            fail_students[student.id] = {
                "info": student_info,
                "subjects": subjects_list,
                "Average Score": "No subjects registered"
            }

    print("\nStudents who Passed:")
    for student in pass_students.values():
        print(f"{student['info']}, Average Score: {student['Average Score']:.2f}, Subjects: {student['subjects']}")

    print("\nStudents who Failed:")
    for student in fail_students.values():
        print(
            f"{student['info']}, Average Score: {student['Average Score']:.2f}, Subjects: {student['subjects']}" if isinstance(
                student['Average Score'],
                float) else f"{student['info']}, {student['Average Score']}, Subjects: {student['subjects']}")

def handle_show_all_students(database):
    students = database.read_students()
    shown_students = set()
    if not students:
        print("No students registered.")
    else:
        for student in students:
            if student.id not in shown_students:
                print(f"Name: {student.name}, ID: {student.id}, Email: {student.email}")
                shown_students.add(student.id)

def handle_remove_student(database):
    student_id = input("Enter student ID to remove: ")
    if database.delete_student(student_id):
        print(f"\033[33mRemoving Student {student_id} Account\033[0m")
    else:
        print(f"\033[31mstudent {student_id} does not exist\033[0m")

def handle_student_login(database):
    print(f"\n\033[32mStudent Login\033[0m")
    email = input("Enter email: ")
    password = input("Enter password: ")
    students = database.read_students()
    found = False
    for student in students:
        if student.email == email:
            found = True
            if student.password == password:
                return student
            else:
                break

    if found:
        print(f"\033[31mLogin failed! Incorrect password.\033[0m")
    else:
        print(f"\033[31mStudent does not exist\033[0m")
    return None

def run():
    db = Database()
    while True:
        choice = main_menu()
        if choice == 'A':
            while True:
                admin_choice = admin_menu()
                if admin_choice == 'C':
                    handle_clear_database(db)
                elif admin_choice == 'G':
                    handle_group_students_by_grade(db)
                elif admin_choice == 'P':
                    handle_partition_students_by_pass_fail(db)
                elif admin_choice == 'R':
                    handle_remove_student(db)
                elif admin_choice == 'S':
                    handle_show_all_students(db)
                elif admin_choice == 'X':
                    break  
        elif choice == 'S':
            while True:  
                student_choice = student_menu()
                if student_choice == 'L':
                    student = handle_student_login(db)
                    if student:
                        while True:
                            sc_choice = student_course_menu(student)
                            if sc_choice == 'C':
                                handle_change_password(student, db)
                            elif sc_choice == 'E':
                                handle_enroll_subject(student, db)
                            elif sc_choice == 'R':
                                handle_drop_subject(student, db)
                            elif sc_choice == 'S':
                                handle_show_subjects(student)
                            elif sc_choice == 'X':
                                break  
                elif student_choice == 'R':
                    handle_student_registration(db)
                elif student_choice == 'X':
                    break  
        elif choice == 'X':
            print("Exiting CLIUniApp...")
            break 


if __name__ == "__main__":
    run()
