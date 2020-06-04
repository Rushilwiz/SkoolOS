from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import os

#list of classes for student; substitute this for Database
classes = {
    "Math": ["week1_hw", "week2_hw", "week3_hw", "unit3_quiz"],
    "English":["journal1", "journal2", "journal3"]
}

#already ccrerrated account through website, has to login
def yesorno(question):
    questions = [
        {
            'type': 'input',
            'name': 'response',
            'message': question,
        },
    ]
    answers = prompt(questions)
    if(answers["response"] == "yes"):
        return True
    return False

def login():
    #enter username
    #enter password
    questions = [
        {
            'type': 'input',
            'name': 'user_name',
            'message': 'What\'s your first name',
        },
        {
            'type': 'password',
            'name': 'passwd',
            'message': 'Password?',
        },
    ]
    answers = prompt(questions)
    print(answers)
    f = open(".login.txt", "w")
    f.write(str(answers["user_name"]))
    print_json(answers)  # use the answers as input for your app

#did not create account through website, has to signup/login
def signup():
    #
    questions = [
        {
            'type': 'input',
            'name': 'first-name',
            'message': 'What\'s your first name',
        },
        {
            'type': 'password',
            'name': 'last-name',
            'message': 'Password?',
        },
        {
            'type': 'list',
            'name': 'last-name',
            'message': 'Grade?',
            'choices':["9","10","11","12"]
        },
        {
            'type': 'input',
            'name': 'user_name',
            'message': 'What\'s your first name',
        },
        {
            'type': 'password',
            'name': 'passwd',
            'message': 'Password?',
        },
    ]
    answers = prompt(questions)
    print(answers)
    f = open(".login.txt", "w")
    f.write(str(answers["user_name"]))
    print_json(answers)  # use the answers as input for your app

def setup():
    #Read classes/assignenments and setup directory:
    #SkoolOS/Math/Week1

if(os.path.exists(".login.txt") == False):
    answer = yesorno("Do you have a SkoolOS account?")
    login()
else:
    print("Hello!")



