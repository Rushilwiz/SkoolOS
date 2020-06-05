from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import json
import os
import argparse


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
            if(user["webmail"] == data[i]["webmail"] and user["password"]) == data[i]["password"]:
                print("Logged in!")
                return data[i]
        print("Error in your submission. Please re-enter")
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
            'message': 'What\'s TJ Webmail?',
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Password?',
        },
    ]
    user = prompt(questions)
    user["classes"] = []
    with open('users.json', 'r') as json_file:
        data = json.load(json_file)
        data.append(user)
        open("users.json", "w").write(str(json.dumps(data)))

def setup(user):
    #Read classes/assignenments and setup directory:
    #SkoolOS/Math/Week1
    for c in user["classes"]:
        os.makedirs(c)
        for a in user["classes"][c]:
            os.makedirs(c + "/" + a)


def start():
    if(os.path.exists(".login.txt") == True):
        b = yesorno("Do you have a SkoolOS account?(y/N)")
        if(b):
            user = login()
            if(user != None):
                setup(user)
        else:
            user = signup()