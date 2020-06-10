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
    output = process.communicate()[1]
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
        if(os.path.isdir(self.username)):
            print("Synced to " +  self.username)
        else:
            os.mkdir(self.username)

                
    #update API and Github, all  assignments / classes
    def update(self):
        #lists all classes
        ignore=['.DS_Store']
        classes = os.listdir(self.username)
        for i in ignore:
            try:
                classes.remove(i)
            except:
                pass

        for i in range(len(classes)):
            c = classes[i]
            path = self.username  +  "/" + c
            #lists all assignments and default files
            #push to git
            isclass = False
            for d in os.listdir(path):
                if(d  == '.git'):
                    isclass=True
                    break
            if(isclass):
                loc = os.getcwd()
                os.chdir(path)
                command('git fetch origin')
                command('git checkout ' + self.username)
                command('git add .')
                command('git commit -m ' + self.username + '-update')
                command('git push -u origin ' + self.username)
                command('git merge master')
                os.chdir(loc)
                print("Updated: " + c)
            else:
                print(d + " is not a class")

    #class name format: <course-name>_<ion_user>


    #add  classes from 'new' field
    def addClass(self, cid):
        if((cid in self.snew) == False):
            if((cid in self.sclass) == True):
                print("Already enrolled in this class.")
            else:
                print("Not added by teacher yet.")
            return None
        data = getDB('http://127.0.0.1:8000/classes/'+cid)

        #clone class repo and make student branch (branch name: username)
        os.chdir(self.username)
        command("git clone " + data['repo'])
        os.chdir(data['name'])
        command("git checkout " + self.username)
        command("git push -u origin " + self.username)

        self.classes.append(data)
        if(len(self.sclass)==0):
            self.sclass = data['id']
        else:
            self.sclass = self.sclass + "," + str(data['id'])

        #upddate self.new
        s=""
        nar = ''
        for i in range(len(self.new)):
            if(self.new[i]['id'] == int(data['id'])):
                print("DELETE: " + self.new[i]['name'])
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
s.update()