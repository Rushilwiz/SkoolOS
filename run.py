from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import os

def login():
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

if(os.path.exists(".login.txt") == False):
    login()
else:
    print("Hello!")



