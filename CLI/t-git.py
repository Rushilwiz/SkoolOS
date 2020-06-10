import subprocess
import os
import requests
import webbrowser
import pprint
import json
import shutil
import time
import pyperclip
from distutils.dir_util import copy_tree


#git clone student directory ==> <student-id>/classes/assignments

#get teacher info from api
def getTeacher(ion_user):
        URL = "http://127.0.0.1:8000/teachers/" + ion_user + "/"
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
    #print(output.decode('utf-8'))

####################################################################################################################################

#public methods: deleteClass, makeClass, update
class Teacher:
    def __init__(self, data):
        # teacher info already  stored in API
        # intitialze fields after GET request
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.git=data['git']
        self.username=data['ion_user']
        self.url= "http://127.0.0.1:8000/teachers/" + self.username + "/"
        self.email = data['email']
        #classes in id form (Example: 4,5)
        
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
        if(os.path.isdir(self.username)):
            print("Synced to " +  self.username)
        else:
            os.mkdir(self.username)

                
    #update API and Github, all  assignments / classes
    def update(self):
        #lists all classes
        ignore=['.git','.DS_Store']
        classes = os.listdir(self.username)
        for i in ignore:
            try:
                classes.remove(i)
            except:
                pass
        #list of classes that have been deleted (not  with  deleteClass)
        extra = []
        for c in self.classes:
            extra.append(c)
        for i in range(len(extra)):
            e = extra[i]['path']
            extra[i] = e
        print("Extra: "+str(extra))
        print("Local:" + str(classes))
        #checks all class directories first
        for c in classes:
            path = self.username  +  "/" + c
            if(self.checkClass(path) == False):
                return
            extra.remove(path)
            print("Current classes: " + path)

        for e in extra:
            self.deleteClass(e)

        for i in range(len(classes)):
            c = classes[i]
            path = self.username  +  "/" + c
            #lists all assignments and default files
            #if  no  .git, directory not synced to  git  or  API
            if (self.checkInDB(path)==False):
                self.addClass(path)
            else:
                #push to git
                loc = os.getcwd()
                os.chdir(path)
                command('git fetch origin')
                command('git pull origin master')
                command('git add .')
                command('git commit -m "Update"')
                command('git push -u origin master')
                os.chdir(loc)

    #class name format: <course-name>_<ion_user>

    #turn existing directory into class, Pre-condition: directory exists
    #relative path to  class: 2022rkhondak/Math4
    def checkClass(self,path):
        cname = path.split("/")
        cname = cname[len(cname)-1]
        if(os.path.isfile(path)):
            print(path + " must be in a Class directory.")
            return False
        if(("_" + self.username) in cname) == False:
            print("Incorrect class name: Must be in the format: " + self.username+ "/<course-name>_<ion_user>, not " + path)
            return False
        dirs = os.listdir(path)
        #checks if there  is a file (not within Assignments) in class, need at least 1
        deffile = False
        #checks if there  is a file in an Assignment, need at least 1 (default True  in case no  assignments)
        as_file = True
        as_bad = ""

        for d in dirs:
            if(os.path.isfile(d)):
                deffile=True
            else:
                #checks if there  is a file in an Assignment, need at least 1
                as_file = False
                asdir = os.listdir(path + "/" + d)
                for a in asdir:
                    if(os.path.isfile(path + "/" + d + "/" +a)):
                        as_file=True
                if(as_file==False):
                    as_bad = d
                    break
        if(as_file==False):
            print("Assignment '" + as_bad + "' does  not  have a default file!")
            return False

        if(deffile==False):
            print("Need a default file in the " + path + " Directory!")
            return  False
        return True
    
    def checkInDB(self, path):
        n  = path.split("/")
        n = n[len(n)-1]
        for c in self.classes:
            if(n == c['name']):
                return True
        return False

    #adds class to  git,  not API
    #Assuming valid  class name
    def addClasstoGit(self, path):
        cname = path.split("/")
        cname = cname[len(cname)-1]
        #push to remote repo
        url='https://github.com/' + self.git + "/" + cname
        if(requests.get(url).status_code != 200):
            input("Make new Git Repo with name: "  + cname + " (Press  any key to continue)\n")
            try:
                pyperclip.copy(cname)
                print(cname + " copied to clipboard.")
            except:
                pass
            time.sleep(2)
            webbrowser.open('https://github.com/new')
            input("Repo created? (Press any key to continue)\n")

            print(url)
            while(requests.get(url).status_code  != 200):
                r = input("Repo not created yet. (Press any key to continue after repo created, or 'N' to exit)\n")
                if(r=="N" or r=="No"):
                    return None
            cdir = os.getcwd()
            os.chdir(path)
            command('git init')
            command('git add .')
            command('git commit -m Hello_Class')
            command('git remote add origin ' + url + '.git')
            command('git push -u origin master')
        else:
            cdir = os.getcwd()
            os.chdir(path)
            print("Repo already exists. Cloning instead.")
            command('git clone')
            command('git fetch origin')
            command('git pull')
            command('git add .')
            command('git commit -m Hello_Class')
            command('git push -u origin master')
        os.chdir(cdir)
        print(cdir)
        data={
            'name':cname,
            'repo':url,
            'path':path,
            'teacher':self.username,
        }
        return data

    #make class from existing directory, add to git and api
    def addClass(self, path):
        if (self.checkClass(path)):
            cname = path.split("/")
            cname = cname[len(cname)-1]
            cpath = self.username + "/" + cname[len(cname)-1]
            data = {
                "name": cname,
                "repo": "",
                "path": cpath,
                "teacher": self.username,
                "assignments": "",
                "default_file": "",
                "confirmed": "",
                "unconfirmed": ""
            }
            #make class instance in db
            data = postDB(data, 'http://127.0.0.1:8000/classes/')
            #add to  instance
            #upate  self.classes
            self.classes.append(data)
            if(len(self.sclass)==0):
                self.sclass = data['id']
            else:
                self.sclass = self.sclass + "," + str(data['id'])
            
            #update teacher instance in db, classes field
            data={
                'first_name':self.first_name,
                'last_name':self.last_name,
                'git':self.git,
                'ion_user':self.username,
                'url':self.url,
                'classes':self.sclass,
                'email':self.email
            }
            putDB(data, self.url)

            return data


    #make a new class from scratch
    #subject: string, assignments: list
    #class name must be: <subject>_<ion_user>
    def makeClass(self, cname, assignments):
        #check if class exists
        path = self.username + "/" + cname
        if(os.path.exists(path)):
            print("Class already exists: " + cname)
            return
        else:
            if((("_" + self.username) in cname) == False):
                print("class name must be: "+ cname + "_" + self.username)
                return
            cdir = os.getcwd()
            os.mkdir(path)
            f=open(path + "/README.md", "w")
            f.close()
            #push to remote repo
            os.chdir(path)
            for a in assignments:
                os.mkdir(a)
                f=open(a + "/instructions.txt", "w")
                f.close()
            os.chdir(cdir)

            data = self.addClass(path)
            return data
    
    def deleteClass(self, path):
        if(os.path.exists(path) == False):
            print(path + " does not exist locally.")
        resp = input("Do you want to delete " + path + " from the SkoolOS system? (y/N) ")
        if(resp != 'y'):
            return

        cname = path.split("/")
        cname = cname[len(cname)-1]
        cid = None
        repo = ''
        for c in self.classes:
            if cname == c['name']:
                cid = str(c['id'])
                repo  =  c['repo']

        #remove from api
        for i in range(len(self.classes)):
            if(self.classes[i]['id'] == int(cid)):
                print("DELETE: " + self.classes[i]['name'])
                del self.classes[i]
                s=""
                #recreate sclass field, using ids
                for c in self.classes:
                    s = s + str(c['id']) + ","
                print(s)
                s = s[:-1]
                print(s)
                data={
                    'first_name':self.first_name,
                    'last_name':self.last_name,
                    'git':self.git,
                    'ion_user':self.username,
                    'url':self.url,
                    'classes':s,
                    'email':self.email
                }
                print(putDB(data, self.url))
                delDB("http://127.0.0.1:8000/classes/" + cid + "/")
                break
        
        #remove locally
        try:
            shutil.rmtree(path)
        except:
            pass
        
        #remove from student directories

#make student repo by student id
    def reqStudent(self, student, classes):
        cid = None
        for c in self.classes:
            print(c['name'])
            if classes == c['name']:
                cid = str(c['id'])
        if(cid==None):
            print(classes +" does not exist.")
            return

        data = getDB("http://127.0.0.1:8000/students/" + student)
        try:
            if(data['added_to']==""):
                data['added_to']=cid
            else:
                data['added_to']=data['added_to']+ "," + cid
        except:
            print(student + " does not exist.")
            return
        print(data['added_to'])
        d={
            'first_name':data["first_name"],
            'last_name':data["last_name"],
            'git':data["git"],
            'ion_user':data["ion_user"],
            'student_id':data["student_id"],
            'added_to':data['added_to'],
            'classes':data["classes"],
            'email':data["email"],
            'grade':data["grade"],
            'completed':data["completed"],
            'repo':data["repo"]
        }
        print(putDB(d, data['url']))
        data1 = getDB("http://127.0.0.1:8000/classes/" + cid)
        if(data1['unconfirmed']==""):
            data1['unconfirmed']=data['ion_user']
        else:
            data1['unconfirmed']=data1['unconfirmed']+ "," + data['ion_user']
        d = {
            "name": classes,
            "repo": "",
            "path": self.username + "/" + classes,
            "teacher": self.username,
            "assignments": "",
            "default_file": "",
            "confirmed": "",
            "unconfirmed": data1['unconfirmed']
        }
        print(putDB(d, data1['url']))

    #confirmed students    
    def addStudent(self, student, classes):
        cdir = os.getcwd()
        cpath = self.username + "/" + classes
        path = "Students/" + classes
        if(os.path.isdir(path) == False):
            os.mkdir(path)
        os.chdir(path)
        student = getDB("http://127.0.0.1:8000/students/" + student)
        command("git clone " + student['repo'])
        os.chdir(cdir)
        copy_tree(cpath, path + "/" + student['ion_user'])
        command('git branch ' + classes)
        command('git add .')
        command('git commit -m Hello')
        command('git push -u origin ' + classes)

    def comment(self):
        print("heheheh")

data = getTeacher("eharris1")
t = Teacher(data)
t.addStudent('2022rkhondak','English11_eharris1')
