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
import webbrowser
import subprocess

from django.conf import settings
import django

from Website.config.settings import DATABASES, INSTALLED_APPS
INSTALLED_APPS.remove('users.apps.UsersConfig')
INSTALLED_APPS.remove('api')
INSTALLED_APPS.remove('skoolos.apps.SkoolosConfig')
INSTALLED_APPS.append('Website.api')
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
django.setup()

from Website.api.models import *

def command(command):
    ar = []
    command = command.split(" ")
    for c in command:
        ar.append(c)
    process = subprocess.Popen(ar, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p=process.poll()
    output = process.communicate()[0]
    print(output.decode('utf-8'))
    return output.decode('utf-8')

class Students:
    def __init__(self, username):
        self.student = Student.objects.get(ion_user = username)
        #ion id: student.user
        if(os.path.isdir(self.student.user) == False):
            if(self.student.repo == ""):
                user= self.student.git
                pwd= input("Enter Github password: ")
                #curl -i -u USER:PASSWORD -d '{"name":"REPO"}' https://api.github.com/user/repos
                url= "curl -i -u " + user + ":" + pwd + " -d '" + '{"name":"' + self.username + '"}' + "' " + "https://api.github.com/user/repos"
                print(url)
                os.system(url)
            cdir = os.getcwd()
            command('git clone https://github.com/' + self.git + '/' + self.username + '.git')
            os.chdir(self.username)
            command('git checkout master')
            command('touch README.md')
            command('git add README.md')
            command('git commit -m "Hello"')
            command('git push -u origin master')
            os.chdir(cdir)
            self.repo = 'https://github.com/' + self.git + '/' + self.username + '.git'
            data={
                'user':self.user,
                'git':self.git,
                'ion_user':self.username,
                'added_to':self.snew,
                'url':self.url,
                'classes':self.sclass,
                'grade':self.grade,
                'completed':self.completed,
                'repo':self.repo
            }
            print(putDB(data, self.url))
        print("Synced to " +  self.username)


# c = {
#     'name':'Math5'
# }

# c = Class.objects.get(name='Math5')
# data = requests.get(url = "http://localhost:8000/api/classes/Math5", auth=('raffukhondaker','hackgroup1')).json()

# r = requests.post(url = "http://localhost:8000/api/classes/", data={'name':'English11', 'teacher':'eharris1', 'owner':2}, auth=('raffukhondaker','hackgroup1')) 

# print("POST:" + str(r.json()))
# # print(r.json())
# # print(c.name)
# # c = {
# #     'classes':c
# # }
# # print(c)
# r = requests.patch(url = "http://localhost:8000/api/teachers/eharris1/", data={'classes':['English11']}, auth=('raffukhondaker','hackgroup1')) 
# print(r.json())
import bgservice.bgservice as bg

bg.watch_dir('2022rkhondak', 'eharris1')
time.sleep(60)
bg.stop_watching()


