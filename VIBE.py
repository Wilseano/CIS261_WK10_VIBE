#Anthony Wilson
#CIS261


import os
import sys


# ---------------------------------------------------------
# Calculate the average of three test scores
# ---------------------------------------------------------
def calculate_average(test1, test2, test3):
    return (test1 + test2 + test3) / 3


# ---------------------------------------------------------
# Determine the letter grade from the student's average
# ---------------------------------------------------------
def calculate_letter_grade(average):
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


# ---------------------------------------------------------
# VIBE helped add input validation so scores must be
# numbers between 0 and 100.
# ---------------------------------------------------------
def get_test_score(test_number):
    while True:
        try:
            score = float(input(f"Enter Test {test_number} score: "))

            if 0 <= score <= 100:
                return score
            else:
                print("Score must be between 0 and 100.")

        except ValueError:
            print("Invalid entry. Please enter a number.")


# ---------------------------------------------------------
# Add a new student
# ---------------------------------------------------------
def add_student(students):
    print("\n--- ADD NEW STUDENT ---")

    name = input("Enter student name: ").strip()
    student_id = input("Enter student ID: ").strip()

    if name == "" or student_id == "":
        print("Student name and ID cannot be blank.")
        return

    # Check for duplicate student ID
    for student in students:
        if student["id"].lower() == student_id.lower():
            print("A student with that ID already exists.")
            return

    test1 = get_test_score(1)
    test2 = get_test_score(2)
    test3 = get_test_score(3)

    average = calculate_average(test1, test2, test3)
    grade = calculate_letter_grade(average)

    student = {
        "name": name,
        "id": student_id,
        "test1": test1,
        "test2": test2,
        "test3": test3,
        "average": average,
        "grade": grade
    }

    students.append(student)

    print("\nStudent added successfully!")
    print(f"Average: {average:.2f}")
    print(f"Letter Grade: {grade}")


# ---------------------------------------------------------
# Display all students in a formatted table
# ---------------------------------------------------------
def display_all_students(students):
    print("\n--- ALL STUDENTS ---")

    if len(students) == 0:
        print("No student records are available.")
        return

    print("-" * 94)
    print(
        f"{'Name':<22}"
        f"{'Student ID':<12}"
        f"{'Test 1':>10}"
        f"{'Test 2':>10}"
        f"{'Test 3':>10}"
        f"{'Average':>12}"
        f"{'Grade':>8}"
    )
    print("-" * 94)

    for student in students:
        print(
            f"{student['name']:<22}"
            f"{student['id']:<12}"
            f"{student['test1']:>10.2f}"
            f"{student['test2']:>10.2f}"
            f"{student['test3']:>10.2f}"
            f"{student['average']:>12.2f}"
            f"{student['grade']:>8}"
        )

    print("-" * 94)


# ---------------------------------------------------------
# Search for a student by name
# Search is case-insensitive as required by the assignment.
# ---------------------------------------------------------
def search_student(students):
    print("\n--- SEARCH FOR STUDENT ---")

    if len(students) == 0:
        print("No student records are available.")
        return

    search_name = input("Enter student name to search for: ").strip().lower()

    matches = []

    for student in students:
        if student["name"].lower() == search_name:
            matches.append(student)

    if len(matches) == 0:
        print("Student not found.")
        return

    print("\nStudent found:")

    for student in matches:
        print(f"Name: {student['name']}")
        print(f"Student ID: {student['id']}")
        print(f"Test 1: {student['test1']:.2f}")
        print(f"Test 2: {student['test2']:.2f}")
        print(f"Test 3: {student['test3']:.2f}")
        print(f"Average: {student['average']:.2f}")
        print(f"Letter Grade: {student['grade']}")
        print()


# ---------------------------------------------------------
# Calculate and display class statistics
# ---------------------------------------------------------
def display_class_statistics(students):
    print("\n--- CLASS STATISTICS ---")

    if len(students) == 0:
        print("No student records are available.")
        return

    averages = []

    for student in students:
        averages.append(student["average"])

    highest_average = max(averages)
    lowest_average = min(averages)
    class_average = sum(averages) / len(averages)

    highest_student = students[averages.index(highest_average)]
    lowest_student = students[averages.index(lowest_average)]

    print(
        f"Highest Average: {highest_average:.2f} "
        f"({highest_student['name']})"
    )

    print(
        f"Lowest Average:  {lowest_average:.2f} "
        f"({lowest_student['name']})"
    )

    print(f"Class Average:   {class_average:.2f}")


# ---------------------------------------------------------
# Save student records to student_grades.txt
#
# Required pipe-delimited format:
# name|id|test1|test2|test3|average|grade
#
# VIBE helped create error handling for file operations.
# ---------------------------------------------------------
def save_students(students):
    try:
        with open("student_grades.txt", "w") as file:
            for student in students:
                file.write(
                    f"{student['name']}|"
                    f"{student['id']}|"
                    f"{student['test1']:.2f}|"
                    f"{student['test2']:.2f}|"
                    f"{student['test3']:.2f}|"
                    f"{student['average']:.2f}|"
                    f"{student['grade']}\n"
                )

        print("Student records saved successfully.")

    except IOError as error:
        print(f"Error saving student records: {error}")


# ---------------------------------------------------------
# Load student records when the program starts
# ---------------------------------------------------------
def load_students():
    students = []

    if not os.path.exists("student_grades.txt"):
        return students

    try:
        with open("student_grades.txt", "r") as file:
            for line in file:
                line = line.strip()

                if line == "":
                    continue

                parts = line.split("|")

                if len(parts) != 7:
                    continue

                try:
                    student = {
                        "name": parts[0],
                        "id": parts[1],
                        "test1": float(parts[2]),
                        "test2": float(parts[3]),
                        "test3": float(parts[4]),
                        "average": float(parts[5]),
                        "grade": parts[6]
                    }

                    students.append(student)

                except ValueError:
                    # Skip damaged or incorrectly formatted records
                    continue

    except IOError as error:
        print(f"Error loading student records: {error}")

    return students


# ---------------------------------------------------------
# Get menu selection.
#
# VIBE was used to improve the original menu so that the
# actual ESC key can be detected in GitHub Codespaces/Linux.
#
# If single-key input is not supported on a computer,
# the program falls back to normal keyboard input.
# ---------------------------------------------------------
def get_menu_choice():
    print("\nSelect an option (1-5) or press ESC: ", end="", flush=True)

    # Windows terminal support
    if os.name == "nt":
        try:
            import msvcrt

            key = msvcrt.getch()

            if key == b"\x1b":
                print("ESC")
                return "ESC"

            choice = key.decode("utf-8")
            print(choice)
            return choice

        except Exception:
            pass

    # Linux / GitHub Codespaces terminal support
    try:
        if sys.stdin.isatty():
            import termios
            import tty

            file_descriptor = sys.stdin.fileno()
            old_settings = termios.tcgetattr(file_descriptor)

            try:
                tty.setraw(file_descriptor)
                key = sys.stdin.read(1)
            finally:
                termios.tcsetattr(
                    file_descriptor,
                    termios.TCSADRAIN,
                    old_settings
                )

            if key == "\x1b":
                print("ESC")
                return "ESC"

            print(key)
            return key

    except Exception:
        pass

    # Fallback if single-key detection is unavailable
    choice = input().strip()

    if choice.lower() in ("esc", "escape"):
        return "ESC"

    return choice


# ---------------------------------------------------------
# Display the main menu
# ---------------------------------------------------------
def display_menu():
    print("\n===================================")
    print("      STUDENT GRADE CALCULATOR")
    print("===================================")
    print("1. Add New Student")
    print("2. Display All Students")
    print("3. Search Student by Name")
    print("4. View Class Statistics")
    print("5. Save and Exit")
    print("ESC. Save and Exit")
    print("===================================")


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------
def main():
    # Load saved records when the program starts
    students = load_students()

    print("===================================")
    print("      STUDENT GRADE CALCULATOR")
    print("===================================")

    if len(students) > 0:
        print(f"{len(students)} student record(s) loaded.")
    else:
        print("No existing student records found.")

    while True:
        display_menu()

        choice = get_menu_choice()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            display_all_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            display_class_statistics(students)

        elif choice == "5":
            print("\nSaving student records...")
            save_students(students)
            print("Thank you for using the Student Grade Calculator.")
            print("Program ended.")
            break

        elif choice == "ESC":
            print("\nESC pressed.")
            print("Saving student records...")
            save_students(students)
            print("Thank you for using the Student Grade Calculator.")
            print("Program ended.")
            break

        else:
            print("Invalid selection. Please choose 1 through 5 or ESC.")


# Start the program
if __name__ == "__main__":
    main()
