import subprocess
import os
import requests


#git clone student directory ==> <student-id>/classes/assignments
def initStudent(ion_user):
    #check if git has already been initialized
    if(os.path.exists(str(ion_user) +"/" + ".git")):
        print("Already synced to: " + str(ion_user))
        return

    #get student repo from API
    URL = "http://127.0.0.1:8000/students/" + ion_user + "/"
    r = requests.get(url = URL, auth=('student','_$YFE#34.9_37jr')) 
    if(r.status_code == 200):
        data = r.json() 
        repo = data['repo']
        classes = data['classes']
        print(data)
        #git clone repo
        process = subprocess.Popen(['git', 'clone', repo], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()

        # make classes directory
        for c in classes:
            cpath = str(ion_user) + "/" + c['name']
            if(os.path.exists(cpath)):
                print(cpath + " already exists...")
            else:
                os.mkdir(str(ion_user) + "/" + c['name'])
            
            #make assignments directory
            for a in c['assignments']:
                path = str(ion_user) + "/" + c['name'] + "/" + a['name']
                print(path)
                if(os.path.exists("/" +path)):
                    print(path + " already exists...")
                else:
                    os.mkdir(str(ion_user) + "/" + c['name'] + "/" + a['name'])
        
        #push to remote repo
        os.chdir(ion_user)
        process = subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()
        process = subprocess.Popen(['git', 'add', '.'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()
        process = subprocess.Popen(['git', 'commit', '-m', "First Commit"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()
        process = subprocess.Popen(['git', 'push', '-u', 'origin','master'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()

    elif(r.status_code == 404):
        print("Make new account!")
    elif(r.status_code == 403):
        print("Invalid username/password")
    else:
        print(r.status_code)

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

initStudent("2022rkhondak")

os.chdir("2022rkhondak")
process = subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
process.wait()
process = subprocess.Popen(['git', 'add', '.'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
process.wait()
process = subprocess.Popen(['git', 'commit', '-m', "First Commit"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
process.wait()
process = subprocess.Popen(['git', 'push', '-u', 'origin','master'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
process.wait()