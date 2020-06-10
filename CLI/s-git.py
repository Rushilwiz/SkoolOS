import subprocess
import os
import requests
import webbrowser
import pprint
import json
import shutil
import time
import pyperclip

#git clone student directory ==> <student-id>/classes/assignments

#get teacher info from api
def getStudent(ion_user):
        URL = "http://127.0.0.1:8000/students/" + ion_user + "/"
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

def command(command):
    ar = []
    command = command.split(" ")
    for c in command:
        ar.append(c)
    process = subprocess.Popen(ar, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p=process.poll()
    output = process.communicate()[0]
    print(output.decode('utf-8'))

####################################################################################################################################

#public methods: deleteClass, makeClass, update
class Student:
    def __init__(self, data):
        # teacher info already  stored in API
        # intitialze fields after GET request
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.git=data['git']
        self.username=data['ion_user']
        self.url= "http://127.0.0.1:8000/students/" + self.username + "/"
        self.email = data['email']
        self.grade = data['grade']
        self.student_id=data['student_id']
        self.completed  = data['completed']
        #classes in id form (Example: 4,5)
        #storing  actual classes
        cid=data['classes'].split(",")
        try:
            cid.remove('')
        except:
            pass
        try:
            cid.remove("")
        except:
            pass
        classes=[]
        for c in cid:
            url = "http://127.0.0.1:8000/classes/" + str(c) + "/"
            classes.append(getDB(url))
        
        self.classes = classes
        self.sclass=str(data['classes'])
        
        #storing  added_to classes
        nid=data['added_to'].split(",")
        try:
            nid.remove('')
        except:
            pass
        try:
            nid.remove("")
        except:
            pass
        nclasses=[]
        for c in nid:
            url = "http://127.0.0.1:8000/classes/" + str(c) + "/"
            nclasses.append(getDB(url))
        
        self.new = nclasses
        self.snew=str(data['added_to'])
        self.repo = data['repo']

        if(os.path.isdir(self.username) == False):
            if(self.repo == ""):
                user= self.git
                pwd= input("Enter Github password: ")
                #curl -i -u USER:PASSWORD -d '{"name":"REPO"}' https://api.github.com/user/repos
                url= "curl -i -u " + user + ":" + pwd + " -d '" + '{"name":"' + self.username + '"}' + "' " + "https://api.github.com/user/repos"
                print(url)
                os.system(url)
            cdir = os.getcwd()
            os.mkdir(self.username)
            os.chdir(self.username)
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
                'first_name':self.first_name,
                'last_name':self.last_name,
                'git':self.git,
                'ion_user':self.username,
                'student_id':self.student_id,
                'added_to':self.snew,
                'url':self.url,
                'classes':self.sclass,
                'email':self.email,
                'grade':self.grade,
                'completed':self.completed,
                'repo':self.repo
            }
            print(putDB(data, self.url))
        print("Synced to " +  self.username)
                
    #update API and Github, all  assignments / classes
    def update(self):
        for c in self.classes:
            data = getDB("http://127.0.0.1:8000/classes/" + str(c['id']))
            os.chdir(self.username + "/" + data['name'])
            command("git checkout -b " + data['name'])
            command("git add " + data['name'])
            command("git commit -m " + data['name'])
            command("git push -u origin " + data['name'])
            command("git pull origin " + data['name'])
        for c in self.new:
            self.addClass(str(c['id']))

    #class name format: <course-name>_<ion_user>


    #add  classes from 'new' field
    def addClass(self, cid):
        if((cid in self.snew) == False):
            if((cid in self.sclass) == True):
                print("Already enrolled in this class.")
            else:
                print("Not added by teacher yet.")
            return None

        data = getDB('http://127.0.0.1:8000/classes/'+ str(cid))
        pwd= input("Enter Github password: ")
        tgit = getDB("http://127.0.0.1:8000/teachers/" + data['teacher'] + "/")['git']
        url= "curl -i -u " + self.git + ":" + pwd + " -X PUT -d '' " + "'https://api.github.com/repos/" + self.git + "/" + self.username + "/collaborators/" + tgit + "'"
        print(url)
        os.system(url)

        data['unconfirmed'] = data['unconfirmed'].replace("," + self.username, "")
        data['unconfirmed'] = data['unconfirmed'].replace(self.username, "")
        data['confirmed'] = data['confirmed'] + "," + self.username
        if(data['confirmed'][0] == ','):
            data['confirmed'] = data['confirmed'][1:]
            print(data['confirmed'])
        print(putDB(data, 'http://127.0.0.1:8000/classes/'+ str(cid) + "/"))

        #add teacher as collaborator 
        #curl -i -u "USER:PASSWORDD" -X PUT -d '' 'https://api.github.com/repos/USER/REPO/collaborators/COLLABORATOR'
        user = self.git

        self.classes.append(data)
        if(len(self.sclass)==0):
            self.sclass = data['id']
        else:
            self.sclass = self.sclass + "," + str(data['id'])

        cdir = os.getcwd()
        path1 = self.username + "/" + self.username
        path2 = self.username
        if(os.path.isdir(path1)):
            os.chdir(path1)
        else:
            os.chdir(self.username)
            command("git clone " + self.repo)
            os.chdir(self.username)

        command("git checkout -b " + data['name'])
        command("touch welcome.txt")
        command("git add welcome.txt")
        command("git commit -m initial")
        command("git push origin " + data['name'])
        #git clone --single-branch --branch <branchname> <remote-repo>
        os.chdir(cdir)
        shutil.move(path1, self.username + "/" + data['name'])
        #upddate self.new
        s=""
        nar = ''
        for i in range(len(self.new)):
            if(self.new[i]['id'] == int(data['id'])):
                del self.new[i]
                #recreate sclass field, using ids
                for c in self.new:
                    s = s + str(c['id']) + ","
                    nar.append(c)
                self.snew=s
                self.new=nar
                break
        
        #update teacher instance in db, classes field
        data={
            'first_name':self.first_name,
            'last_name':self.last_name,
            'git':self.git,
            'ion_user':self.username,
            'student_id':self.student_id,
            'added_to':self.snew,
            'url':self.url,
            'classes':self.sclass,
            'email':self.email,
            'grade':self.grade,
            'completed':self.completed
        }
        print(self.url)
        print(putDB(data, self.url))
        return data
    
    def submit(self, path):
        #2022rkhondak/English11_eharris1/Essay1
        #check if valid assignment
        parts = path.split("/")
        if(len(parts) != 3):
            print("Assignment path too short")
            return
        isclass = False
        for c in  self.classes:
            if(c['name'] == parts[1]):
                isclass==True
                break
        if(parts[0] != self.username  and isclass and os.path.isdir(path) == False):
            print("Not valid assignment")
            return
        if((parts[1] + "/" + parts[2]) in self.completed):
            print(parts[2] + " already submited. ")
            # return
        resp = input("Are you sure you want to submit? You cannot do this again.(y/N) ")
        if(resp == 'y'):
            os.chdir(self.username + "/" + parts[1])
            command("git add .")
            command("git commit -m submit")
            command("git tag " + parts[1] + "-final")
            command("git push -u origin " + self.username + " --tags")
            self.completed = self.completed + "," + parts[1] + "/" + parts[2]
            data={
                'first_name':self.first_name,
                'last_name':self.last_name,
                'git':self.git,
                'ion_user':self.username,
                'student_id':self.student_id,
                'added_to':self.snew,
                'url':self.url,
                'classes':self.sclass,
                'email':self.email,
                'grade':self.grade,
                'completed':self.completed
            }
            #print(putDB(data, "http://127.0.0.1:8000/students/" + self.username + "/"))

data = getStudent("2022rkhondak")
s = Student(data)
#s.update()