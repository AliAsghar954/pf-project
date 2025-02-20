import json

def isValidCourseCode(code):
    return len(code) == 5 and code[:2].isalpha() and code[2:].isdigit()

def isValidCourseName(name):
    return name.replace(" ", "").isalpha() and len(name) <= 50

def isValidCreditHours(crdHrs):
    return 1 <= crdHrs <= 3

def isValidSemester(semester):
    return 1 <= semester <= 8

def loadCourses():
    try:
        with open("courses.json", "r") as file:
            data = file.read().strip()
            return json.loads(data) if data else {"codeList": [], "nameList": [], "crtHrsList": [], "semList": []}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"codeList": [], "nameList": [], "crtHrsList": [], "semList": []}

def saveCourses(data):
    with open("courses.json", "w") as file:
        json.dump(data, file)         

def loadStudents():
    try:
        with open("students.json", "r") as file:
            data = file.read().strip()
            return json.loads(data) if data else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def saveStudents(data):
    with open("students.json", "w") as file:
        json.dump(data, file)

def registerStudent(students, studentID, password):
    if studentID in students:
        print("Student ID already exists.")
    else:
        students[studentID] = password
        saveStudents(students)
        print("Student registered successfully.")

def loginStudent(students, studentID, password):
    if students.get(studentID) == password:
        print("Login successful.")
        return True
    else:
        print("Invalid ID or password.")
        return False

def AddCourse(data, courseCode, courseName, crdHrs, semester):
    data["codeList"].append(courseCode)
    data["nameList"].append(courseName)
    data["crtHrsList"].append(crdHrs)
    data["semList"].append(semester)
    saveCourses(data)
    print("Course has been added successfully.")

def EditCourse(data, courseCode, courseName, crdHrs, semester):
    if courseCode in data["codeList"]:
        idx = data["codeList"].index(courseCode)
        data["nameList"][idx] = courseName
        data["crtHrsList"][idx] = crdHrs
        data["semList"][idx] = semester
        saveCourses(data)
        print("Course has been edited successfully.")
    else:
        print("Course code not found.")

def DeleteCourse(data, courseCode):
    if courseCode in data["codeList"]:
        idx = data["codeList"].index(courseCode)
        data["codeList"].pop(idx)
        data["nameList"].pop(idx)
        data["crtHrsList"].pop(idx)
        data["semList"].pop(idx)
        saveCourses(data)
        print("Course has been deleted successfully.")
    else:
        print("Course code not found.")

def ViewCourses(data):
    print("Course Code\tName\t\t\tCredit Hours\tSemester")
    for code, name, crdHrs, semester in zip(data["codeList"], data["nameList"], data["crtHrsList"], data["semList"]):
        print(f"{code}\t{name}\t\t{crdHrs}\t{semester}")

def ViewSemesterCourses(data, semester):
    print("Course Code\tName\t\t\tCredit Hours")
    for code, name, crdHrs, sem in zip(data["codeList"], data["nameList"], data["crtHrsList"], data["semList"]):
        if sem == semester:
            print(f"{code}\t{name}\t\t{crdHrs}")

students = loadStudents()
data = loadCourses()

while True:
    print("** Welcome to University Learning Management System **")
    print("Choose the following option")
    print("1 Register Student")
    print("2 Student Login")
    print("3 Add Course")
    print("4 Update Course")
    print("5 Delete Course")
    print("6 View All Courses")
    print("7 View Courses of a Semester")
    print("8 Exit Program")

    option = input("Choose the option: ")

    if option == "1":
        studentID = input("Enter student ID: ")
        password = input("Enter password: ")
        registerStudent(students, studentID, password)

    elif option == "2":
        studentID = input("Enter student ID: ")
        password = input("Enter password: ")
        loginStudent(students, studentID, password)

    elif option == "3":
        courseCode = input("Enter course code: ")
        courseName = input("Enter course name: ")
        try:
            crdHrs = int(input("Enter credit hours: "))
            semester = int(input("Enter semester: "))

            if (isValidCourseCode(courseCode) and isValidCourseName(courseName)
                    and isValidCreditHours(crdHrs) and isValidSemester(semester)):
                AddCourse(data, courseCode, courseName, crdHrs, semester)
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numeric values for credit hours and semester.")

    elif option == "4":
        courseCode = input("Enter the course code to edit: ")
        if courseCode in data["codeList"]:
            courseName = input("Enter new course name: ")
            try:
                crdHrs = int(input("Enter new credit hours: "))
                semester = int(input("Enter new semester: "))

                if (isValidCourseCode(courseCode) and isValidCourseName(courseName)
                        and isValidCreditHours(crdHrs) and isValidSemester(semester)):
                    EditCourse(data, courseCode, courseName, crdHrs, semester)
                else:
                    print("Invalid input. Please try again.")
            except ValueError:
                print("Invalid input. Please enter numeric values for credit hours and semester.")
        else:
            print("Course code not found.")

    elif option == "5":
        courseCode = input("Enter the course code to delete: ")
        DeleteCourse(data, courseCode)

    elif option == "6":
        ViewCourses(data)

    elif option == "7":
        try:
            semester = int(input("Enter the semester: "))
            if isValidSemester(semester):
                ViewSemesterCourses(data, semester)
            else:
                print("Invalid semester. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for semester.")

    elif option == "8":
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")
