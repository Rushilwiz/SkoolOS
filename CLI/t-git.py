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
    print(output.decode('utf-8'))

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
        if(os.path.isdir(self.username + "/Students")):
            print("Synced to " +  self.username)
        else:
            os.makedirs(self.username + "/Students")

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
                self.sclass = data['name']
            else:
                self.sclass = self.sclass + "," + str(data['name'])
            
            #update teacher instance in db, classes field
            teacher={
                'first_name':self.first_name,
                'last_name':self.last_name,
                'git':self.git,
                'ion_user':self.username,
                'url':self.url,
                'classes':self.sclass,
                'email':self.email
            }
            putDB(teacher, self.url)

            return teacher


    #make a new class from scratch
    #subject: string, assignments: list
    #class name must be: <subject>_<ion_user>
    def makeClass(self, cname, assignments):
        #check if class exists
        path = self.username + "/" + cname
        isclass = False
        acourses = getDB("http://127.0.0.1:8000/classes/")['results']
        for c in acourses:
            if c['name'] == cname:
                isclass=True
                break
        if(os.path.exists(path) or isclass):
            print("Class already exists: " + cname)
            if(isclass):
                print("Class already exists in Database")
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
        repo = ''
        print("DELETE: " + self.classes[i]['name'])
        for i in range(len(self.classes)):
            c = self.classes[i]
            if(c['name'] == cname):
                del self.classes[i]
                s=""
                #recreate sclass field, using ids
                for c in self.classes:
                    s = s + str(c['name']) + ","
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
                delDB("http://127.0.0.1:8000/classes/" + cname + "/")
                break
        
        #remove locally
        try:
            shutil.rmtree(path)
        except:
            pass
        
        #remove from student directories


    def isStudent(self, student):
        r = requests.get(url = "http://127.0.0.1:8000/students/" + student + "/", auth=('raffukhondaker','hackgroup1')) 
        if(r.status_code != 200):
            return False
        return True

    def reqStudent(self, sname, cname):
        if(self.isStudent(sname) == False):
            print(sname + " does not exist.")
            return
        course = getDB("http://127.0.0.1:8000/classes/" + cname)
        if(sname in course['unconfirmed']):
            print (sname + " already requested.")
            return
        if(sname in course['confirmed']):
            print (sname + " alredy enrolled.")
            return
        
        student = getDB("http://127.0.0.1:8000/students/" + sname)
        try:
            if(student['added_to']==""):
                student['added_to']=course['name']
            else:
                student['added_to']=student['added_to']+ "," + course['name']
        except:
            print(sname + " does not exist.")
            return
        print(student['added_to'])
        s={
            'first_name':student["first_name"],
            'last_name':student["last_name"],
            'git':student["git"],
            'ion_user':student["ion_user"],
            'student_id':student["student_id"],
            'added_to':student['added_to'],
            'classes':student["classes"],
            'email':student["email"],
            'grade':student["grade"],
            'completed':student["completed"],
            'repo':student["repo"]
        }
        student = putDB(s, student['url'])
        
        if(course['unconfirmed']==""):
            course['unconfirmed']=student['ion_user']
        else:
            course['unconfirmed']=course['unconfirmed']+ "," + student['ion_user']
        cinfo = {
            "name": course['name'],
            "repo": "",
            "path": self.username + "/" + course['name'],
            "teacher": self.username,
            "assignments": "",
            "default_file": "",
            "confirmed": course["confirmed"],
            "unconfirmed": course['unconfirmed']
        }
        print(putDB(cinfo, course['url']))

    #Student should have confirmed on their endd, but class had not been updated yet
    #git clone confirmed student repo, copy files into repo and push branch
    def addStudent(self, sname, cname):
        if(self.isStudent(sname) == False):
            print(sname + " does not exist.")
            return

        student = getDB("http://127.0.0.1:8000/students/" + sname)
        course = getDB("http://127.0.0.1:8000/classes/" + cname)

        if((student['ion_user'] in course['unconfirmed']) == False):
            print("Student has not been requested to join yet.")
            return
        if((cname in student['added_to']) == True or (cname in student['classes']) == False):
            print("Student has not confirmed class yet")
            return
        if(os.path.exists(self.username + "/Students/" + cname + "/" + student['ion_user']) or (student['ion_user'] in course['confirmed']) == True):
            print("Student already added to class")
                
        #git clone and make student/class directories
        cdir = os.getcwd()
        cpath = self.username + "/" + cname
        path = self.username + "/Students/" + cname
        spath = self.username + "/Students/" + cname + "/" + student['ion_user']
        if(os.path.isdir(path) == False):
            os.makedirs(path)
        if(os.path.isdir(spath) == False):
            os.chdir(path)
            command("git clone " + student['repo'])
            os.chdir(cdir)

        #push to git
        copy_tree(cpath, path + "/" + student['ion_user'])
        os.chdir(spath)
        command('git checkout ' + cname)
        command('git pull origin ' + cname)
        command('git add .')
        command('git commit -m Hello')
        command('git push -u origin ' + cname)
        command('git checkout master')

        if(course['confirmed']==""):
            course['confirmed']=student['ion_user']
        else:
            course['confirmed']=course['confirmed']+ "," + student['ion_user']
        cinfo = {
            "name": course['name'],
            "repo": "",
            "path": course['path'],
            "teacher": course['name'],
            "assignments": "",
            "default_file": "",
            "confirmed": course["confirmed"],
            "unconfirmed": course['unconfirmed']
        }
        print(putDB(cinfo, course['url']))

    def addAssignment(self, path, course):
        parts = path.split("/")
        aname = parts[len(parts)-1]
        if(os.path.isdir(path) == 0 or len(parts) < 3) or aname in self.sclass:
            print("Not valid path.")
            return
        if((parts[1] in self.sclass) == False):
            print("Not in valid class directory")
            return
        ar  = [x[2] for x in os.walk(path)]
        print(ar)
        for folder in ar:
            if len(folder) == 0:
                print("Assignment is completely empty, need a file.")
                return
        course = getDB("http://127.0.0.1:8000/classes/" + course)
        slist = os.listdir(os.getcwd() + "/" + self.username + "/Students/" + course['name'])
        cdir = os.getcwd()
        for st in slist:
            if st in course['confirmed']:
                spath =  os.path.join(os.getcwd() + "/" + self.username + "/Students/" + course['name'], st)
                if(os.path.exists(spath + "/" + aname) == False):
                    os.mkdir(spath + "/"  + aname)
                    print(st)
                    print(copy_tree(path, spath + "/" + aname))
                    os.chdir(spath)
                    command('git checkout ' + course['name'])
                    command('git pull origin ' + course['name'])
                    command('git add .')
                    command('git commit -m Hello')
                    command('git push -u origin ' + course['name'])
                    os.chdir(cdir)
                else:
                    print(st + " already has assignment")

    def getHistory(self, student, course):
        course = getDB("http://127.0.0.1:8000/classes/" + course)
        try:
            if((student in course['confirmed']) == False):
                print("Student not in class")
                return
        except:
            print("class does not exist")
            return
        os.chdir(self.username + "/Students/" + course['name'] + "/" + student)
        process = subprocess.Popen(['git', 'log', course['name']], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p=process.poll()
        output = process.communicate()[0].decode('utf-8')
        print(output)

    def comment(self):
        print("heheheh")
    
    def updateAssignnment():
        print()

data = getTeacher("eharris1")
t = Teacher(data)
t.getHistory("2022rkhondak", "English11_eharris1")
