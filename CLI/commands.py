from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import json
import os
import argparse

'''
my_parser = argparse.ArgumentParser(prog='skool', description='Let SkoolOS control your system', epilog="Try again")
my_parser.add_argument('--init', action="store_true") #returns true if run argument
args = my_parser.parse_args()

update()
outputs = vars(args)
if(outputs['init']):
    start()
'''


# already created account through website, has to login
def update():
    """
    Gets data from the database
    :return:
    """
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
    if answers["response"] == "y":
        return True
    return False


def login():
    """
    Login to the website with a username and password
    :return: user information json if successful, None otherwise
    """
    # enter username
    # enter password
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
    # reading from json of users (replace w GET to database) to check if user is registered
    with open('users.json', 'r') as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            if user["webmail"] == data[i]["webmail"]:
                if user["password"] == data[i]["password"]:
                    print("Logged in!")
                    return data[i]
                else:
                    print("Password incorrect. Try again.")
                    return None
        print("User not found. Please Try again")
        return None


# did not create account through website, has to signup/login
def signup():
    """
    Used to create an account for the service.
    Called if the user does not have an existing account and must create one.
    :return: the new user account
    """
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
            'choices': ["9", "10", "11", "12"]
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
    if not ("@tjhsst.edu" in user['webmail']):
        print("Webmail entered was not a @tjhhsst.edu. Try again.")
        return None

    user["classes"] = []
    with open('users.json', 'r') as json_file:
        data = json.load(json_file)
        data.append(user)
        open("users.json", "w").write(str(json.dumps(data)))
    return user


def relogin():
    """
    Login to an already verified user account
    :return:
    """
    questions = [
        {
            'type': 'list',
            'name': 'choice',
            'message': '',
            'choices': ["Continue as current user", "Login into new user", "Sign up into new account"]
        },
    ]
    answer = prompt(questions)


def setup(user):
    # Read classes/assignenments and setup directory:
    # SkoolOS/Math/Week1
    """
    Reads classes and assignments of/for the user and properly sets of their work directory
    :param user:
    :return:
    """
    for c in user["classes"]:
        os.makedirs(c)
        for a in user["classes"][c]:
            os.makedirs(c + "/" + a)


def start():
    """
    Prompts the user for whether or not they have an account and allows them to login/signup depending on their response
    :return:
    """
    if not os.path.exists(".login.txt"):
        b = yesorno("Do you have a SkoolOS account?(y/N)")
        if b:
            user = login()
            if user is not None:
                setup(user)
                open(".login.txt", "w").write(str(user))
        else:
            user = signup()
            if user is not None:
                open(".login.txt").write(str(user))
