import subprocess
import os
import requests
import webbrowser
import pprint
import json

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
    return r.json()

def postDB(data, url):
    r = requests.post(url = url, data=data, auth=('raffukhondaker','hackgroup1')) 
    return(r.status_code)
def putDB(data, url):
    r = requests.put(url = url, data=data, auth=('raffukhondaker','hackgroup1')) 
    return(r.status_code)

def command(command):
    ar = []
    command = command.split(" ")
    for c in command:
        ar.append(c)
    process = subprocess.Popen(ar, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p=process.poll()
    output = process.communicate()[0]
    #print(output.decode('utf-8'))

class Teacher:
    def __init__(self, data):
        # teacher info already  stored in API
        # intitialze fields after GET request
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.git=data['git']
        self.username=data['ion_user']
        self.url= "http://127.0.0.1:8000/teachers/" + self.username + "/"
        self.classes=data['classes'].split(" ")
        self.sclass=data['classes']
        if(os.path.isdir(self.username)):
            print("Already synced to " +  self.username)
        else:
            os.mkdir(self.username)
                
    def checkGit(self, ass):
        for a in ass:
            if a =='.git':
                return True
        return False

    #update API and Github, all  assignments / classes
    def update(self):
        #lists all classes
        classes = os.listdir(self.username)

        #checks all class directories first
        for c in classes:
            path = self.username  +  "/" + c
            if(self.checkClass(path) == False):
                return
        cdict = []
        for c in classes:
            path = self.username  +  "/" + c
            #lists all assignments and default files
            ass =  os.listdir(path)
            #if  no  .git, directory not synced to  git  or  API
            if (self.checkGit(ass)==False):
                data = self.addClasstoGit(path)
                postDB(data, 'http://127.0.0.1:8000/classes/')
            else:
                #push to git
                loc = os.getcwd()
                os.chdir(path)
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
        if(("_" + self.username) in cname) == False:
            print("Incorrect class name: Must be in the format: <course-name>_<ion_user>")
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
            if(os.path.isdir(d)) and d != '.git':
                #checks if there  is a file in an Assignment, need at least 1
                as_file = False
                asdir = os.listdir(d)
                for a in asdir:
                    if(os.path.isfile(a)):
                        as_file=True
                if(as_file==False):
                    as_bad = a
                    break
        if(as_file==False):
            print("Assignment '" + as_bad + "' does  not  have a default file!")
            return False

        if(deffile==False):
            print("Need a default file in the " + path + " Directory!")
            return  False
        return True

    #adds class to  git,  not API
    def addClasstoGit(self, path):
        cname = path.split("/")
        cname = cname[len(cname)-1]
        #push to remote repo
        url='https://github.com/' + self.git + "/" + cname
        if(self.checkClass(path)):
            if(requests.get(url).status_code != 200):
                input("Make new Git Repo with name: "  + cname + " (Press  any key to continue)\n")
                webbrowser.open('https://github.com/new')
                input("Repo created? (Press any key to continue)\n")

                print(url)
                while(requests.get(url).status_code  != 200):
                    print(requests.get(url))
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
            os.chdir(cdir)
            data={
                'name':cname,
                'repo':url,
                'path':path,
                'teacher':self.username
            }
            return data
        return None


    #make a new class from scratch
    #subject: string, assignments: list
    #class name must be: <subject>_<ion_user>
    def makeClass(self, cname, assignments):
        cdir = os.getcwd()
        os.chdir(self.username)
        #check if class exists
        if(os.path.exists(cname)):
            print("Class already exists: " + cname)
            return
        else:
            if((("_" + self.username) in cname) == False):
                print("class name must be: "+ cname + "_" + self.username)
                return
            path = self.username + "/" + cname
            os.mkdir(cname)
            f=open(cname + "/README.md", "w")
            f.close()
            #push to remote repo
            os.chdir(cname)
            for a in assignments:
                os.mkdir(a)
                f=open(a + "/instructions.txt", "w")
                f.close()
            os.chdir(cdir)

            data = self.addClasstoGit(path)
            print(postDB(data, 'http://127.0.0.1:8000/classes/'))
            if(len(self.sclass)==0):
                classes = cname
            else:
                classes = self.sclass + "," + cname

            data={
                'first_name':self.first_name,
                'last_name':self.last_name,
                'git':self.git,
                'ion_user':self.username,
                'url':self.url,
                'classes':classes
            }
            print(putDB(data, self.url))
            return data

#make student repo by student id
    def addStudent(self,stid):
        print(stid)

    def comment(self):
        print("heheheh")

data = getTeacher("eharris1")
t = Teacher(data)
t.makeClass('Math4_eharris1', ['Week1_HW', 'Week2_HW'])


