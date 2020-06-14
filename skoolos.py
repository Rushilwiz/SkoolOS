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
import os
import argparse

client_id = r'QeZPBSKqdvWFfBv1VYTSv9iFGz5T9pVJtNUjbEr6'
client_secret = r'0Wl3hAIGY9SvYOqTOLUiLNYa4OlCgZYdno9ZbcgCT7RGQ8x2f1l2HzZHsQ7ijC74A0mrOhhCVeZugqAmOADHIv5fHxaa7GqFNtQr11HX9ySTw3DscKsphCVi5P71mlGY'
redirect_uri = 'http://localhost:8000/callback/'
token_url = 'https://ion.tjhsst.edu/oauth/token/'
scope = ["read"]
USER = ""
PWD = ""

def main():
    print("")
    print("░██████╗██╗░░██╗░█████╗░░█████╗░██╗░░░░░  ░█████╗░░██████╗")
    print("██╔════╝██║░██╔╝██╔══██╗██╔══██╗██║░░░░░  ██╔══██╗██╔════╝")
    print("╚█████╗░█████═╝░██║░░██║██║░░██║██║░░░░░  ██║░░██║╚█████╗░")
    print("░╚═══██╗██╔═██╗░██║░░██║██║░░██║██║░░░░░  ██║░░██║░╚═══██╗")
    print("██████╔╝██║░╚██╗╚█████╔╝╚█████╔╝███████╗  ╚█████╔╝██████╔╝")
    print("╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝  ░╚════╝░╚═════╝░")
    print("")

    if not os.path.exists(".profile"):
        try:
            URL = "http://127.0.0.1:8000/api/"
            r = requests.get(url = URL, auth=('raffukhondaker','hackgroup1'))
            print("End service at http://127.0.0.1:8000/ before continuing.")
            sys.exit(0)
        except:
            pass
        input("Welcome to SkoolOS. Press any key to create an account")
        authenticate()
    else:
        try:
            URL = "http://127.0.0.1:8000/api/"
            r = requests.get(url = URL, auth=('raffukhondaker','hackgroup1')) 
        except:
            print("Start Django server first")
            sys.exit(0)
        f = open('.profile','r')
        data = json.loads(f.read())
        f.close()
        PWD = data['password']
        USER = data['username']
        if(data['is_student']):
            studentCLI()
        else:
            teacherCLI()
        


    # while True:
    #     pass
def studentCLI():
    from CLI import student
    data = getStudent(USER)
    print(data)
    student = student.Student(data)
    print(student)

def teacherCLI():
    from CLI.teacher import Teacher
    print("fail")

def getStudent(ion_user):
        URL = "http://127.0.0.1:8000/api/students/" + ion_user + "/"
        r = requests.get(url = URL, auth=('raffukhondaker','hackgroup1')) 
        if(r.status_code == 200):
            data = r.json() 
            return data
        elif(r.status_code == 404):
            return None
            print("Make new account!")
        elif(r.status_code == 403):
            return None
            print("Invalid username/password")
        else:
            return None
            print(r.status_code) 

def getDB(url):
    r = requests.get(url = url, auth=('raffukhondaker','hackgroup1')) 
    print("GET:" + str(r.status_code))
    return(r.json())

def postDB(data, url):
    r = requests.post(url = url, data=data, auth=('raffukhondaker','hackgroup1')) 
    print("POST:" + str(r.status_code))
    return(r.json())

def putDB(data, url):
    r = requests.put(url = url, data=data, auth=('raffukhondaker','hackgroup1'))
    print("PUT:" + str(r.status_code))
    return(r.json())

def delDB(url):
    r = requests.delete(url = url, auth=('raffukhondaker','hackgroup1'))
    print("DELETE:" + str(r.status_code))
    return None

def makePass():
    questions = [
    {
        'type': 'password',
        'name': 'pwd',
        'message': 'Enter SkoolOS Password (NOT ION PASSWORD): ',
    },
    ]
    pwd = prompt(questions)['pwd']
    while(len(pwd) < 7):
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
    while(not pwd == pwd2):
        print("Passwords do not match.")
        pwd2 = prompt(conf)['pwd']
    else:
        print("PASSWORD SAVED")
        return pwd

def authenticate():
    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://ion.tjhsst.edu/oauth/authorize/")

    cdir = os.getcwd()
    #Linux: chromdriver-linux
    #Macos: chromdriver-mac
    #Windows: chromdriver.exe
    if('CLI' in os.getcwd()):
        path = os.path.join(os.getcwd(), '../','chromedriver-mac')
    else:
        path = os.path.join(os.getcwd(), 'chromedriver-mac')

    browser = webdriver.Chrome(path)
    web_dir = os.path.join(os.getcwd(), 'CLI', 'oauth')
    print(web_dir)
    os.chdir(web_dir)
    if os.path.exists("index.html"):
        os.remove("index.html")

    template = open("template.html", "r")
    index = open("index.html", "w")
    for line in template:
        index.write(line.replace('AUTH_URL', authorization_url))
    template.close()
    index.close()

    server = Thread(target=create_server)
    server.daemon = True
    server.start()

    browser.get("localhost:8000/")

    while "http://localhost:8000/callback/?code" not in browser.current_url:
        time.sleep(0.25)

    url = browser.current_url
    gets = url_decode(url.replace("http://localhost:8000/callback/?", ""))
    while "http://localhost:8000/callback/?code" not in browser.current_url:
        time.sleep(0.25)

    url = browser.current_url
    gets = url_decode(url.replace("http://localhost:8000/callback/?", ""))
    code = gets.get("code")
    if state == gets.get("state"):
        state = gets.get("state")
        print("states good")
    browser.quit()

    #print(code)
    print(state)

    payload = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri, 'client_id': client_id,
               'client_secret': client_secret, 'csrfmiddlewaretoken': state}
    token = requests.post("https://ion.tjhsst.edu/oauth/token/", data=payload).json()
    #print(token)
    headers = {'Authorization': f"Bearer {token['access_token']}"}

    # And finally get the user's profile!
    profile = requests.get("https://ion.tjhsst.edu/api/profile", headers=headers).json()
    
    #pprint.pprint(profile)
    username = profile['ion_username']
    email = profile['tj_email']
    first_name = profile['first_name']
    last_name = profile['last_name']
    is_student = profile['is_student']
    password = ""
    #password creation

    profile = {
        'username':username,
        'email':email,
        'first_name':first_name,
        'last_name':last_name,
        'is_student':is_student,
        'password':password,
    }
    os.chdir(cdir)

    profileFile = open(".profile", "w")
    profileFile.write(json.dumps(profile))
    profileFile.close()

    #try to make password
    password = makePass()
    profile['password'] = password
    profileFile = open(".profile", "w")
    profileFile.write(json.dumps(profile))
    profileFile.close()

    sys.exit

def create_server():
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    print("serving at port:" + str(port))
    httpd.serve_forever()

if __name__ == "__main__":
    main()
