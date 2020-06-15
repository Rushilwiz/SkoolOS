import os
import subprocess
import requests
import webbrowser
import pprint
import json
import shutil
import time
import pyperclip
from distutils.dir_util import copy_tree
from datetime import datetime 

#git clone student directory ==> <student-id>/classes/assignments

#get teacher info from api
def getTeacher(ion_user):
        URL = "http://127.0.0.1:8000/api/teachers/" + ion_user + "/"
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
        self.git=data['git']
        self.username=data['ion_user']
        self.url= "http://127.0.0.1:8000/api/teachers/" + self.username + "/"
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
            url = "http://127.0.0.1:8000/api/classes/" + str(c) + "/"
            classes.append(getDB(url))
        
        self.classes = classes
        self.sclass=str(data['classes'])
        if(os.path.isdir(self.username + "/Students")):
            print("Synced to " +  self.username)
        else:
            os.makedirs(self.username + "/Students")

        #2020-05-11 12:25:00

        

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
            cpath = self.username + "/" + cname
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
            data = postDB(data, 'http://127.0.0.1:8000/api/classes/')
            #add to  instance
            #upate  self.classes
            self.classes.append(data)
            if(len(self.sclass)==0):
                self.sclass = data['name']
            else:
                self.sclass = self.sclass + "," + str(data['name'])
            
            #update teacher instance in db, classes field
            teacher={
                'git':self.git,
                'ion_user':self.username,
                'url':self.url,
                'classes':self.sclass,
            }
            putDB(teacher, self.url)

            return teacher


    #make a new class from scratch
    #subject: string, assignments: list
    #class name must be: <subject>_<ion_user>
    def makeClass(self, cname):
        #check if class exists
        path = self.username + "/" + cname
        isclass = False
        acourses = getDB("http://127.0.0.1:8000/api/classes/")['results']
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
            # os.chdir(path)
            # for a in assignments:
                
            #     os.mkdir(a)
            #     f=open(a + "/instructions.txt", "w")
            #     f.close()
            # os.chdir(cdir)

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
                    'git':self.git,
                    'ion_user':self.username,
                    'url':self.url,
                    'classes':s,
                }
                print(putDB(data, self.url))
                delDB("http://127.0.0.1:8000/api/classes/" + cname + "/")
                break
        
        #remove locally
        try:
            shutil.rmtree(path)
        except:
            pass
        
        #remove from student directories


    def isStudent(self, student):
        r = requests.get(url = "http://127.0.0.1:8000/api/students/" + student + "/", auth=('raffukhondaker','hackgroup1')) 
        if(r.status_code != 200):
            return False
        return True

    def reqStudent(self, sname, cname):
        if(self.isStudent(sname) == False):
            print(sname + " does not exist.")
            return False
        course = getDB("http://127.0.0.1:8000/api/classes/" + cname)
        if(sname in course['unconfirmed']):
            print (sname + " already requested.")
            return True
        if(sname in course['confirmed']):
            print (sname + " alredy enrolled.")
            return False
        
        student = getDB("http://127.0.0.1:8000/api/students/" + sname)
        try:
            if(student['added_to']==""):
                student['added_to']=course['name']
            else:
                student['added_to']=student['added_to']+ "," + course['name']
        except:
            print(sname + " does not exist.")
            return False
        print(student['added_to'])
        s={
            'git':student["git"],
            'ion_user':student["ion_user"],
            'added_to':student['added_to'],
            'classes':student["classes"],
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
            "assignments": course['assignments'],
            "default_file": "",
            "confirmed": course["confirmed"],
            "unconfirmed": course['unconfirmed']
        }
        print(putDB(cinfo, course['url']))
        return True
            
    #Student should have confirmed on their endd, but class had not been updated yet
    #git clone confirmed student repo, copy files into repo and push branch
    def addStudent(self, sname, cname):
        if(self.isStudent(sname) == False):
            print(sname + " does not exist.")
            return False

        student = getDB("http://127.0.0.1:8000/api/students/" + sname)
        course = getDB("http://127.0.0.1:8000/api/classes/" + cname)

        if(os.path.exists(self.username + "/Students/" + cname + "/" + student['ion_user']) or (student['ion_user'] in course['confirmed']) == True):
            print(student['ion_user'] + " already added to class")
            return True
        if((cname in student['added_to']) == True or (cname in student['classes']) == False):
            print(student['ion_user']+ " has not confirmed class yet")
            return False
        if((student['ion_user'] in course['unconfirmed']) == False):
            print(course['unconfirmed'])
            print(student['ion_user']+" has not been requested to join yet.")
            return False
                
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
        os.chdir(spath)
        command('git checkout ' + cname)
        command('git pull origin ' + cname)
        os.chdir(cdir)
        copy_tree(cpath, path + "/" + student['ion_user'])
        os.chdir(spath)
        command('git add .')
        command('git commit -m Hello')
        command('git push -u origin ' + cname)
        os.chdir(cdir)

        if(course['confirmed']==""):
            course['confirmed']=student['ion_user']
        else:
            course['confirmed']=course['confirmed']+ "," + student['ion_user']

        #only 1 pereson on confirmeed
        if(("," in course['unconfirmed']) == False):
            course['unconfirmed']=""
        #mutiple
        else:
            course['unconfirmed']= course['unconfirmed'].replace("," + student['ion_user'], "")
            course['unconfirmed']= course['unconfirmed'].replace(student['ion_user']+",", "")

        cinfo = {
            "name": course['name'],
            "repo": "",
            "path": course['path'],
            "teacher": self.username,
            "assignments": course['assignments'],
            "default_file": "",
            "confirmed": course["confirmed"],
            "unconfirmed": course['unconfirmed']
        }
        print(putDB(cinfo, course['url']))
        return True

    #goes through list of studennts, tries to add, then request, return unconfirmed students
    def reqAddStudentList(self, array, cname):
        unconf = []
        for i in range(len(array)):
            a = array[i]
            if(self.addStudent(a, cname) == False):
                self.reqStudent(a, cname)
                unconf.append(a)
        return unconf

    #add local path to student directory, make new instance in api
    def addAssignment(self, path, course, due):
        parts = path.split("/")
        aname = parts[len(parts)-1]

        if(os.path.isdir(path) == 0 or len(parts) < 3) or aname in self.sclass:
            print("Not valid path.")
            return False
        if((parts[1] in self.sclass) == False):
            print("Not in valid class directory")
            return False
        #parts of assignment name (Essay1, APLit)
        if((course in aname) == False):
            print("Assignment named incorrectly; could be "+ aname + "_" + course)
            return False
    
        ar  = [x[2] for x in os.walk(path)]
        print(ar)
        for folder in ar:
            if len(folder) == 0:
                print("Assignment is completely empty, needs a file.")
                return False
        p1 = course.split("_")[0]
        if(p1 in aname == False):
            print(aname + "incorrectly formated: must be " + aname + "_" + p1 + ".")
            return False
        try:
            datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
        except:
            print("Due-date format is incorrect")
            return False
        
        course = getDB("http://127.0.0.1:8000/api/classes/" + course)
        if(aname in course['assignments']):
            print("Assignment name already taken.")
            return False
    
        print(course['assignments'])
        input()
        #################### FINISH VERIFYING

        if(os.path.exists(os.getcwd() + "/" + self.username + "/Students/" + course['name']) == False):
            print("No students in this class yet")
            return True
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
        
        #check if assignment already exists
        r = requests.get(url = 'http://127.0.0.1:8000/api/assignments/' + aname, auth=('raffukhondaker','hackgroup1')) 
        if(r.status_code != 200):
            ass = {
                'name': aname,
                'path':path,
                'classes':course['name'],
                'teacher':self.username,
                'due_date':due
            }
            postDB(ass, 'http://127.0.0.1:8000/api/assignments/')
            if(course['assignments'] == ""):
                course['assignments'] = aname
            else:
                course['assignments'] = course['assignments'] + "," + aname
                
            cinfo = {
                "name": course['name'],
                "repo": "",
                "path": course['path'],
                "teacher": "eharris1",
                "assignments": course['assignments'],
                "default_file": "",
                "confirmed": course["confirmed"],
                "unconfirmed": course['unconfirmed']
            }
            putDB(cinfo, "http://127.0.0.1:8000/api/classes/" + course['name'] + "/")
            return True
        else:
            print("Assignment already addedd")
            return True
    
    #try to avoid
    #copy modified assignments to student directories
    def updateAssignment(self, path, course, due):
        if(os.path.isdir(path) == False):
            print(path + " is not an assignment.")
            return
        try:
            if(due != None or due == ""):
                datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
        except:
            print("Due-date format is incorrect")
            return
        input()
        parts = path.split("/")
        aname =  parts[len(parts)-1]
        course = getDB("http://127.0.0.1:8000/api/classes/" + course)
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

    #pull student's work, no modifications
    def getStudents(self, course):
        if((course in self.sclass) == False):
            print(course + " not a class.")
            return
        path = self.username + "/Students/" + course 
        slist = os.listdir(path)
        cdir = os.getcwd()
        for st in slist:
            os.chdir(path + "/" + st)
            command('git checkout ' + course)
            command('git pull origin ' + course)
            os.chdir(cdir)

    def getCommits(self, student, course, commits):
        course = getDB("http://127.0.0.1:8000/api/classes/" + course)
        try:
            if((student in course['confirmed']) == False):
                print("Student not in class")
                return
        except:
            print("class does not exist")
            return

        cdir = os.getcwd()
        os.chdir(self.username + "/Students/" + course['name'] + "/" + student)
        process = subprocess.Popen(['git', 'log', '-' + str(commits), course['name']], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p=process.poll()
        output = process.communicate()[0].decode('utf-8').split('\n\n')
        months = ['Jan', 'Feb', 'Mar', "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        fout = []
        for i in range(len(output)):
            if("Date" in output[i]):
                c = output[i].split("\n")
                for k in range(len(c)):
                    temp = []
                    if('commit' in c[k]):
                        c[k] = c[k].replace('commit', '').strip()
                    elif('Date:' in c[k]):
                        c[k] = c[k].replace('Date:', '').strip()
                date = c[2].split(" ")
                times = date[3].split(":")
                mon = -1
                for m in range(len(months)):
                    if date[1] == months[m]:
                        mon = m
                d1 = datetime(int(date[4]), mon, int(date[2]), int(times[0]), int(times[1]))
                #datetime1 = datetime.strptime('07/11/2019 02:45PM', '%m/%d/%Y %I:%M%p')
                fout.append([c[0],d1])
                #output[i] = [c[0], d1]
                #print(output[i])
        print(fout)
        os.chdir(cdir)
        return fout
    
    def getChanges(self, student, course, commits):
        course = getDB("http://127.0.0.1:8000/api/classes/" + course + "/")
        ar = self.getCommits(student, course['name'], commits)
        commit = ar[len(ar)-1][0]
        start = ""
        print("END:" + commit)
        print("START: " + start)
        cdir = os.getcwd()
        os.chdir(self.username + "/Students/" + course['name'] + "/" + student)
        process = subprocess.Popen(['git', 'diff', commit, '--name-status'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p=process.poll()
        output = process.communicate()[0].decode('utf-8')
        print(output)
        os.chdir(cdir)
        
        '''
        assignment = {
            'name': English11_eharris1,
            'due_date': 2020-06-11 16:58:33.383124
        }
        '''
        #check if assignment changed after due date
    def afterSubmit(self, course, assignment, student):
        
        assignment = getDB("http://127.0.0.1:8000/api/assignments/" + assignment)
        # assignment = {
        #     'name': assignment,
        #     'due_date': "2020-04-11 16:58:33.383124",
        #     'classes':course
        # }
        log = self.getCommits(student, course, 30)
        assignment['due_date'] = datetime.strptime(assignment['due_date'], '%Y-%m-%d %H:%M:%S.%f')
        late = False
        cdir = os.getcwd()
        os.chdir(self.username + "/Students/" + course + "/" + student)
        for l in log:
            process = subprocess.Popen(['git', 'show', l[0]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            p=process.poll()
            output = process.communicate()[0].decode('utf-8')
            if(assignment['name'] in output):
                print(l[1])
                print(assignment['due_date'])
                print("--------------")
                if(l[1] > assignment['due_date']):
                    print("LATE")
                    os.chdir(cdir)
                    return True
        print("On time")
        os.chdir(cdir)
        return False

    def comment(self):
        print("heheheh")


data = getTeacher("eharris1")
t = Teacher(data)
# t.makeClass("APLit_eharris1")
#t.addAssignment("eharris1/APLit_eharris1/Lab3_APLit_eharris1", "APLit_eharris1", '2020-08-11 16:58:33.383124')
#ar = ['2022rkhondak','2022inafi','2023rumareti']
#extra = t.reqAddStudentList(ar, "APLit_eharris1")
#print(extra)
# t.getStudents('2022rkhondak')
# t.getChanges('2022rkhondak','APLit_eharris1', 10)

'''
TO-DO
- More checks
    - add students to APLit_eharris1
    - make new class, make newe assignment, add/req students, make assignment
- Add assignment to class after being made
- Check if assignment name is taken
- getUsage  on student
    - comit history
    - check differences between commits
    - check if student changes file after submissionn deadline
'''

