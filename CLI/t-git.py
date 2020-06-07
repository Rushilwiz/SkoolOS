import subprocess
import os
import requests


#git clone student directory ==> <student-id>/classes/assignments
def initTeacher(student_id):
    #check if git has already been initialized
    if(os.path.exists(str(student_id) +"/" + ".git")):
        print("Already synced to: " + str(student_id))
        return

    #get student repo from API
    URL = "http://127.0.0.1:8000/students/" + str(student_id) + "/"
    r = requests.get(url = URL, auth=('student','_$YFE#34.9_37jr')) 
    data = r.json() 
    repo = data['repo']
    classes = data['classes']
    print(classes)
    #git clone repo
    process = subprocess.Popen(['git', 'clone', repo], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.communicate()

    #make classes directory
    for c in classes:
        cpath = str(student_id) + "/" + c['name']
        if(os.path.exists(cpath)):
            print(cpath + " already exists...")
        else:
            os.mkdir(str(student_id) + "/" + c['name'])
        
        #make assignments directory
        for a in c['assignments']:
            path = str(student_id) + "/" + c['name'] + "/" + a['name']
            print(path)
            if(os.path.exists("/" +path)):
                print(path + " already exists...")
            else:
                os.mkdir(str(student_id) + "/" + c['name'] + "/" + a['name'])

#Teachers

#make student repo by student id
def addStudent(stid, teacher):
    os.mkdir(stid)
    os.chdir(os.getcwd() + "/" + stid)
    process = subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.communicate()
    process = subprocess.Popen(['git', 'add', '.'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.communicate()
    process = subprocess.Popen(['git', 'commit', '-m', "First Commit"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    process.communicate()

def addStudents(filename):
    print(filename)

def addAsignment(name):
    print(name)

def updateAssignment(name):
    print(name)

def comment(filename, text):
    print(text)


initStudent(1579460)