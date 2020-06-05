from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import json
import os
import argparse


#already ccrerrated account through website, has to login
def update():
    #get data from database
    return

def yesorno(question):
    questions = [
        {
            'type': 'input',
            'name': 'response',
            'message': question,
        },
    ]
    answers = prompt(questions)
    if(answers["response"] == "y"):
        return True
    return False

def login():
    #enter username
    #enter password
    questions = [
        {
            'type': 'input',
            'name': 'webmail',
            'message': 'What\'s TJ Webmail',
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Password?',
        },
    ]
    user = prompt(questions)
    #reading from json of users (replace w GET to database) to check if user is registered
    with open('users.json', 'r') as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            if user["webmail"] == data[i]["webmail"]:
                if(user["password"] == data[i]["password"]):
                    print("Logged in!")
                    return data[i]
                else:
                    print("Password incorrect. Try again.")
                    return None
        print("User not found. Please Try again")
        return None

#did not create account through website, has to signup/login
def signup():
    questions = [
        {
            'type': 'input',
            'name': 'first-name',
            'message': 'What\'s your first name',
        },
        {
            'type': 'input',
            'name': 'last-name',
            'message': 'What\'s your last name?',
        },
        {
            'type': 'list',
            'name': 'grade',
            'message': 'Grade?',
            'choices':["9","10","11","12"]
        },
        {
            'type': 'input',
            'name': 'webmail',
            'message': 'What\'s your TJ Webmail?',
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Password?',
        },
    ]
    user = prompt(questions)
    for i in user:
        if user[i] == "":
            print("Some forms were left blank. Try again.\n")
            return None
    if len(user["password"]) < 6:
        print("Password is too short. Try again.")
        return None
    if (("@tjhsst.edu" in user['webmail']) == False):
        print("Webmail entered was not a @tjhhsst.edu. Try again.")
        return None

    user["classes"] = []
    with open('users.json', 'r') as json_file:
        data = json.load(json_file)
        data.append(user)
        open("users.json", "w").write(str(json.dumps(data)))
    return user

def relogin():
    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': '',
            'choices':["Continue as current user","Login into new user","Sign up into new account"]
        },
    ]
    answer = prompt(questions)
    

def setup(user):
    #Read classes/assignenments and setup directory:
    #SkoolOS/Math/Week1
    for c in user["classes"]:
        os.makedirs(c)
        for a in user["classes"][c]:
            os.makedirs(c + "/" + a)

def start():
    if(os.path.exists(".login.txt") == False):
        b = yesorno("Do you have a SkoolOS account?(y/N)")
        if(b):
            user = login()
            if(user != None):
                setup(user)
                open(".login.txt", "w").write(str(user))
        else:
            user = signup()
            if(user != None):
                open(".login.txt").write(str(user))

        