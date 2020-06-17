"""
The main program file for SkoolOS
"""
import sys
from urllib.parse import urlparse
import requests
from requests_oauthlib import OAuth2Session
from selenium import webdriver
import os.path
import time
import http.server
import socketserver
from threading import Thread
from werkzeug.urls import url_decode
import pprint
from PyInquirer import prompt, print_json
import json
import datetime
import os
import argparse
import webbrowser

client_id = r'QeZPBSKqdvWFfBv1VYTSv9iFGz5T9pVJtNUjbEr6'
client_secret = r'0Wl3hAIGY9SvYOqTOLUiLNYa4OlCgZYdno9ZbcgCT7RGQ8x2f1l2HzZHsQ7ijC74A0mrOhhCVeZugqAmOADHIv5fHxaa7GqFNtQr11HX9ySTw3DscKsphCVi5P71mlGY'
redirect_uri = 'http://localhost:8000/callback/'
token_url = 'https://ion.tjhsst.edu/oauth/token/'
scope = ["read"]
USER = ""
PWD = ""


def main():
    """
    The Command Line Interface (CLI) for SkoolOS
    Serves to allow both teachers and students to access the majority of the features of SkoolOS
    """
    print("")
    print("░██████╗██╗░░██╗░█████╗░░█████╗░██╗░░░░░  ░█████╗░░██████╗")
    print("██╔════╝██║░██╔╝██╔══██╗██╔══██╗██║░░░░░  ██╔══██╗██╔════╝")
    print("╚█████╗░█████═╝░██║░░██║██║░░██║██║░░░░░  ██║░░██║╚█████╗░")
    print("░╚═══██╗██╔═██╗░██║░░██║██║░░██║██║░░░░░  ██║░░██║░╚═══██╗")
    print("██████╔╝██║░╚██╗╚█████╔╝╚█████╔╝███████╗  ╚█████╔╝██████╔╝")
    print("╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝  ░╚════╝░╚═════╝░")
    print("")

    profiles = os.listdir()

    if not ("profile" in str(profiles)):
        try:
            URL = "http://127.0.0.1:8000/api/"
            r = requests.get(url=URL)
        except:
            print("Run Django server on http://127.0.0.1:8000/ before continuing")
            sys.exit(0)

        input("Welcome to SkoolOS. Press any key to create an account")
        # webbrowser.open("http://127.0.0.1:8000/login", new=2)
        authenticate()
    profiles = os.listdir()
    users = []
    info = []
    count = 1
    for i in range(len(profiles)):
        p = profiles[i]
        if 'profile' in p:
            f = open(p, 'r')
            d = json.loads(f.read())
            f.close()
            info.append(d)
            users.append(str(count) + ") " + d['username'])
            count = count + 1
    users.append(str(count) + ") Make new user")
    user = [
        {
            'type': 'list',
            'name': 'user',
            'choices': users,
            'message': 'Select User: ',
        },
    ]
    u = int(prompt(user)['user'].split(")")[0]) - 1
    if u + 1 == count:
        authenticate()
        return
    data = info[u]
    PWD = data['password']
    USER = data['username']
    print(data['username'])
    if data['is_student']:
        studentCLI(USER, PWD)
    else:
        teacherCLI(USER, PWD)


#################################################################################################### STUDENT METHODS

def studentCLI(user, password):
    """
    The CLI for students to access
    @param user: student username
    @param password: student password
    """
    from CLI import student
    data = getUser(user, password, 'student')
    student = student.Student(data, password)
    student.update()
    EXIT = False
    while not EXIT:
        course = chooseClassStudent(student)
        if course == "Exit SkoolOS":
            return
        EXIT = classOptionsStudent(student, course)


# return class
def chooseClassStudent(student):
    """
    Chooses a class for a student to view and work on
    @param student: a student
    :return: a course prompt
    """
    carray = student.sclass.split(",")
    if len(carray) == 1 and carray[0] == "":
        carray.remove("")
        print("No classes")

    carray.append("Exit SkoolOS")
    courses = [
        {
            'type': 'list',
            'name': 'course',
            'choices': carray,
            'message': 'Select class: ',
        },
    ]
    course = prompt(courses)['course']
    print(course)
    return course


def classOptionsStudent(student, course):
    """
    Allows students to choose what they want to do related to a class
    The student can save, exit, or go back
    @param student: a student
    @param course: a course
    :return: True if exiting, False if going back
    """
    student.viewClass(course)
    student.getAssignments(course,  100)
    choices = ["Save","Submit assignment","Back","Exit SkoolOS"]
    options = [
        {
            'type': 'list',
            'name': 'option',
            'choices': choices,
            'message': 'Select: ',
        },
    ]
    option = prompt(options)['option']
    if option == "Save":
        student.update()
        print("Saved!")
        classOptionsStudent(student, course)
    if option == "Back":
        student.exitCLI()
        # dont exit cli
        return False
    if option == "Exit SkoolOS":
        student.exitCLI()
        # exit cli
        return True
    if(option == "Submit assignment"):
        assignments = os.listdir(student.username)
        tlist = []
        b = True
        for a in assignments:
            oname = a + "_" + course            
            a = student.username + "/" + a
            if(os.path.isdir(a) and not "." in a and not oname in student.completed):
                tlist.append(a)
        assignments = tlist
        assignments.append("Back")
        print(assignments)
            
        options = [
        {
            'type': 'list',
            'name': 'submit',
            'choices':assignments,
            'message': 'Select: ',
        },
        ]
        ass = prompt(options)['submit']
        if(ass == "Back"):
            return False
        else:
            student.submit(course, ass)
            return False


#################################################################################################### TEACHER METHODS
def teacherCLI(user, password):
    """
    The CLI for teachers to access
    @param user: teachers username
    @param password: teachers password
    """
    from CLI import teacher
    data = getUser(user, password, 'teacher')
    print(data)
    teacher = teacher.Teacher(data, password)
    EXIT = False
    # 1. make a class
    # 2. add studeents to an existing class
    # 3. Get progress logs on a student
    # 2. make an assignment for a class
    # 3. view student submissions for an assignment
    while not EXIT:
        # Options: '1) Request Student', "2) Add assignment", "3) View student information", "4) Exit"
        course = chooseGeneralTeacher(teacher)
        if course == "Exit SkoolOS":
            EXIT = True
        elif course == "Make New Class":
            EXIT = makeClassTeacher(teacher)
        # selected a class
        else:
            #Pull confirmed students directory
            teacher.getStudents(course)
            option = classOptionsTeacher(teacher, course)
            if option == '1':
                EXIT = addStudentsTeacher(teacher, course)
            elif option == '2':
                EXIT = addAssignmentTeacher(teacher, course)
            elif option == '3':
                EXIT = viewStudentsTeacher(teacher, course)
            else:
                EXIT = True


def chooseGeneralTeacher(teacher):
    carray = []
    for c in teacher.classes:
        carray.append(c)
    carray.append("Make New Class")
    carray.append("Exit SkoolOS")
    courses = [
        {
            'type': 'list',
            'name': 'course',
            'choices': carray,
            'message': 'Select class: ',
        },
    ]
    course = prompt(courses)['course']
    return course


def makeClassTeacher(teacher):
    questions = [
        {
            'type': 'input',
            'name': 'cname',
            'message': 'Class Name (Must be: <subject>_<ion_user>): ',
        },
    ]
    cname = prompt(questions)['cname']
    print(cname)
    while not ("_" + teacher.username) in cname:
        print("Incorrect naming format")
        questions = [
            {
                'type': 'input',
                'name': 'cname',
                'message': 'Class Name (Must be: <subject>_<ion_user>): ',
            },
        ]
        cname = prompt(questions)['cname']

    teacher.makeClass(cname)
    soption = ["1) Add individual student", "2) Add list of students through path", "3) Exit"]
    questions = [
        {
            'type': 'list',
            'choices': soption,
            'name': 'students',
            'message': 'Add Students): ',
        },
    ]
    choice = prompt(questions)['students'].split(")")[0]
    if "1" == choice:
        s = input("Student name: ")
        teacher.addStudent(s, cname)
    if "2" == choice:
        print("File must be .txt and have 1 student username per line")
        path = input("Relative Path: ")
        while not os.path.exists(path):
            if path == 'N':
                return True
            print(path + " is not a valid path")
            path = input("Enter file path ('N' to exit): ")
        f = open(path, 'r')
        students = f.read().splitlines()
        teacher.reqAddStudentList(students, cname)
        return False


def classOptionsTeacher(teacher, course):
    print("Class: " + course)
    unconf = getDB(teacher.username, teacher.password, "http://localhost:8000/api/classes/" + course)['unconfirmed']
    for s in unconf:
        teacher.addStudent(s, course)
    options = ['1) Request Student', "2) Add assignment", "3) View student information", "4) Exit"]
    questions = [
        {
            'type': 'list',
            'name': 'course',
            'choices': options,
            'message': 'Select option: ',
        },
    ]
    option = prompt(questions)['course'].split(")")[0]
    return option


def addStudentsTeacher(teacher, course):
    soption = ["1) Add individual student", "2) Add list of students through path", "3) Exit"]
    questions = [
        {
            'type': 'list',
            'choices': soption,
            'name': 'students',
            'message': 'Add list of students (input path): ',
        },
    ]
    schoice = prompt(questions)['students'].split(")")[0]
    if schoice == '1':
        questions = [
            {
                'type': 'input',
                'name': 'student',
                'message': 'Student Name: ',
            },
        ]
        s = prompt(questions)['student']
        teacher.reqStudent(s, course)
        return False
    if schoice == '2':
        questions = [
            {
                'type': 'input',
                'name': 'path',
                'message': 'Path: ',
            },
        ]
        path = prompt(questions)['path']
        while not os.path.exists(path):
            if path == 'N':
                sys.exit(0)
            print(path + " is not a valid path")
            path = input("Enter file path ('N' to exit): ")
        f = open(path, 'r')
        students = f.read().splitlines()
        teacher.reqAddStudentList(students, course)
        return False
    else:
        return True


def addAssignmentTeacher(teacher, course):
    nlist = os.listdir(teacher.username + "/" + course)
    alist = getDB(teacher.username, teacher.password, "http://localhost:8000/api/classes/" + course)['assignments']
    print(nlist)
    tlist = []
    b = True
    for n in nlist:
        b = True
        print(teacher.username + "/" + course + "/" + n)
        for a in alist:
            if n in a or n == a:
                # print("Assignments: " + n)
                b = False
        if not os.path.isdir(teacher.username + "/" + course + "/" + n):
            b = False
        if b:
            tlist.append(n)

    nlist = tlist
    if len(nlist) == 0:
        print("No new assignments found")
        print(
            "To make an assignment: make a subdirectory in the " + course + " folder. Add a file within the new folder")
        return False
    questions = [
        {
            'type': 'list',
            'choices': nlist,
            'name': 'assignment',
            'message': 'Select new assignment: ',
        },
    ]
    ass = prompt(questions)['assignment']
    apath = teacher.username + "/" + course + "/" + ass
    due = input("Enter due date (Example: 2020-08-11 16:58): ")
    due = due + ":33.383124"
    due = due.strip()
    f = False
    while not f:
        try:
            datetime.datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
            f = True
        except:
            print("Due-date format is incorrect.")
            print(due)
            due = input("Enter due date (Example: 2020-08-11 16:58): ")
            due = due + ":33.383124"
    teacher.addAssignment(apath, course, due)
    return False


def viewStudentsTeacher(teacher, course):
    data = getDB(teacher.username, teacher.password, "http://127.0.0.1:8000/api/classes/" + course)
    students = data["confirmed"]
    unconf = data['unconfirmed']
    print("Studented in class: ")
    for s in students:
        print(s)
    print("Requsted Students: ")
    for s in unconf:
        print(s)
    student = input("View student (Enter student's ion username): ")
    while((not student in str(data['confirmed'])) and (not student in str(data['unconfirmed']))):
        print("Student not affiliated with class")
        student = input("View student ('N' to exit): ")
        if student == 'N':
            return False
    sinfo = getDB(teacher.username, teacher.password, "http://127.0.0.1:8000/api/students/" + student + "/")
    pprint.pprint(sinfo)
    print("Confirmed: " + str(student in str(data['confirmed'])))
    if(student in str(data['confirmed'])):
        path = teacher.username + "/Students/" + course + "/" + student
        print(student + "'s work: " + path)
        fin = sinfo['completed'].split(",")
        alist = []
        for f in fin:
            if(course in f):
                late = teacher.afterSubmit(course, f, student)
                if(late):
                    s = f.split("_")[0] + " (LATE)"
                else:
                    s = f.split("_")[0]
                alist.append(s)
        print("Has submitted: " + str(alist))

    #put log stuff

############################################################################################################################################


def getUser(ion_user, password, utype):
    """
    Returns user information
    @param ion_user: user
    @param password: user's password
    @param utype: type of user (student or teacher
    :return: api user information
    """
    if 'student' in utype:
        URL = "http://127.0.0.1:8000/api/students/" + ion_user + "/"
    else:
        URL = "http://127.0.0.1:8000/api/teachers/" + ion_user + "/"
        print(URL)
    r = requests.get(url=URL, auth=(ion_user, password))
    print(r.json())
    if r.status_code == 200:
        data = r.json()
        print(200)
        return data
    elif r.status_code == 404:
        print("Make new account!")
        return None
    elif r.status_code == 403:
        print("Invalid username/password")
        return None
    else:
        print(r.status_code)
        return None


def patchDB(USER, PWD, url, data):
    """
    Sends a PATCH request to url
    @param USER: username
    @param PWD: password
    @param url: URL for request
    @param data: data to request
    :return: json request response
    """
    r = requests.patch(url=url, data=data, auth=(USER, PWD))
    print("PATH:" + str(r.status_code))
    return r.json()


def getDB(USER, PWD, url):
    """
    Sends a GET request to url
    @param USER: username
    @param PWD: password
    @param url: URL for request
    :return: json request response
    """
    r = requests.get(url=url, auth=(USER, PWD))
    print("GET:" + str(r.status_code))
    return r.json()


def postDB(USER, PWD, url, data):
    """
    Sends a POST request to url
    @param USER: username
    @param PWD: password
    @param url: URL for request
    @param data: data to request
    :return: json request response
    """
    r = requests.post(url=url, data=data, auth=(USER, PWD))
    print("POST:" + str(r.status_code))
    return r.json()


def putDB(USER, PWD, url, data):
    """
    Sends a PUT request to url
    @param USER: username
    @param PWD: password
    @param url: URL for request
    @param data: data to request
    :return: json request response
    """
    r = requests.put(url=url, data=data, auth=(USER, PWD))
    print("PUT:" + str(r.status_code))
    return r.json()


def delDB(USER, PWD, url):
    """
    Sends a DELETE request to url
    @param USER: username
    @param PWD: password
    @param url: URL for request
    :return: json request response
    """
    r = requests.delete(url=url, auth=(USER, PWD))
    print("DELETE:" + str(r.status_code))
    return None


def makePass():
    """
    Prompts the user to create a password
    :return: the password
    """
    questions = [
        {
            'type': 'password',
            'name': 'pwd',
            'message': 'Enter SkoolOS Password (NOT ION PASSWORD): ',
        },
    ]
    pwd = prompt(questions)['pwd']
    while len(pwd) < 7:
        print("Password too short (Must be over 6 characters)")
        pwd = prompt(questions)['pwd']
    conf = [
        {
            'type': 'password',
            'name': 'pwd',
            'message': 'Re-enter password: ',
        },
    ]
    pwd2 = prompt(conf)['pwd']
    while not pwd == pwd2:
        print("Passwords do not match.")
        pwd2 = prompt(conf)['pwd']
    else:
        print("PASSWORD SAVED")
        return pwd


def authenticate():
    """
    Authenticates the user via Ion OAuth
    """
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")
    import os
    cdir = os.getcwd()
    # Linux: chromdriver-linux
    # Macos: chromdriver-mac
    # Windows: chromdriver.exe
    print("OS: ")
    print("MacOS")
    print("Linux")

    system = input("Enter OS: ")
    while(system.lower() != "linux" and system.lower() != "macos"):
        print("Not valid OS")
        system = input("Enter OS: ")
    if(system.lower() == 'macos'):
        path = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver-mac')
    if(system.lower() == 'linux'):
        path = os.path.join(os.getcwd(), 'chromedriver', 'chromedriver-linux')
    
    browser = webdriver.Chrome(path)

    browser.get("localhost:8000/login")

    # while "http://localhost:8000/callback/?code" not in browser.current_url:
    #     time.sleep(0.25)

    url = browser.current_url
    gets = url_decode(url.replace("http://localhost:8000/login/?", ""))
    while "http://localhost:8000/login/?username=" not in browser.current_url and (
            not browser.current_url == "http://localhost:8000/"):  # http://localhost:8000/
        time.sleep(0.25)

    url = browser.current_url
    gets = url_decode(url.replace("http://localhost:8000/login/?username=", ""))
    # code = gets.get("code")
    # if state == gets.get("state"):
    #     state = gets.get("state")
    #     print("states good")
    browser.quit()
    questions = [
        {
            'type': 'input',
            'name': 'username',
            'message': 'Enter SkoolOS Username (Same as ION Username): ',
        },
        {
            'type': 'password',
            'name': 'pwd',
            'message': 'Enter SkoolOS Password (NOT ION PASSWORD): ',
        },
    ]
    data = prompt(questions)
    pwd = data['pwd']
    user = data['username']
    r = requests.get(url="http://localhost:8000/api/", auth=(user, pwd))
    while r.status_code != 200:
        print("INCORRECT LOGIN CREDENTIALS")
        r = requests.get(url="http://localhost:8000/api/", auth=(user, pwd))
        data = prompt(questions)
        pwd = data['pwd']
        user = data['username']
        print(r.status_code)
    r = requests.get(url="http://localhost:8000/api/students/" + user + "/", auth=(user, pwd))
    is_student = False
    if r.status_code == 200:
        is_student = True
        print("Welcome, student " + user)
        r = requests.get(url="http://localhost:8000/api/students/" + user + "/", auth=(user, pwd))
        profile = r.json()
        username = profile['ion_user']
        grade = profile['grade']
        profile = {
            'username': username,
            'grade': grade,
            'is_student': is_student,
            'password': pwd,
        }
        fname = "." + username + "profile"
        profileFile = open(fname, "w")
        profileFile.write(json.dumps(profile))
        profileFile.close()

    else:
        print("Welcome, teacher " + user)
        r = requests.get(url="http://localhost:8000/api/teachers/" + user + "/", auth=(user, pwd))
        profile = r.json()
        username = profile['ion_user']
        profile = {
            'username': username,
            'is_student': is_student,
            'password': pwd,
        }
        fname = "." + username + "profile"
        profileFile = open(fname, "w")
        profileFile.write(json.dumps(profile))
        profileFile.close()

    sys.exit(0)


def create_server():
    """
    Creates a simple HTTP server for creating api requests from the CLI
    """
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving at port:" + str(port))
    httpd.serve_forever()


if __name__ == "__main__":
    main()
