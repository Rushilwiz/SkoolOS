import subprocess
import os
import requests


#git clone student directory ==> <student-id>/classes/assignments
'''
{
            "url": "http://127.0.0.1:8000/teachers/eharris1/",
            "first_name": "Errin",
            "last_name": "Harris",
            "classes": [
                {
                    "url": "http://127.0.0.1:8000/classes/1/",
                    "name": "Math5",
                    "assignments": [
                        {
                            "name": "Week1_HW",
                            "due_date": "2020-06-07T07:46:30.537197Z",
                            "url": "http://127.0.0.1:8000/assignments/1/",
                            "files": [
                                {
                                    "name": "instructions.txt"
                                }
                            ]
                        },
                        {
                            "name": "Week2_HW",
                            "due_date": "2020-06-07T07:46:30.548596Z",
                            "url": "http://127.0.0.1:8000/assignments/2/",
                            "files": [
                                {
                                    "name": "instructions.txt"
                                }
                            ]
                        }
                    ],
                    "repo": ""
                }
            ],
            "git": "therealraffi",
            "ion_user": "eharris1"
        },
'''
#get teacher info from api
def getData(ion_user):
        URL = "http://127.0.0.1:8000/students/" + ion_user + "/"
        r = requests.get(url = URL, auth=('student','_$YFE#34.9_37jr')) 
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

class Teacher:
    def __init__(self, data):
        # teacher info already  stored in API
        # intitialze fields after GET request
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.classes=data['classes']
        self.git=data['git']
        self.username=data['ion_user']
        self.url= "http://127.0.0.1:8000/teachers/" + self.username + "/"
        self.data=data

        if(os.path.exists(self.username )):
            print("Already synced to: " + str(self.username))
            return
        os.mkdir(self.username)
        classes = self.classes
        # make classes directory
        for c in classes:
            cname= c['name'] + "_" + self.username
            cpath = self.username + "/" + cname
            if(os.path.exists(cpath)):
                print(cpath + " already exists...")
            else:
                #make class directory
                os.mkdir(cpath)
                #make default files for each class
                for filename in c['default_file']:
                    f=open(cpath+"/"+filename, "w")
                    f.close()
                
                #make assignments directory
                for a in c['assignments']:
                    path = cpath + "/" + a['name']
                    print(path)
                    if(os.path.exists(path)):
                        print(path + " already exists...")
                    else:
                        os.mkdir(path)
                        f=open(path + "/README.md", "w")
                        f.close()

                #push to remote repo
                os.chdir(cpath)
                process = subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process.wait()
                process = subprocess.Popen(['git', 'add', '.'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process.wait()
                process = subprocess.Popen(['git', 'commit', '-m', "Hello Class!"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process.wait()
                #git remote add origin git@github.com:alexpchin/<reponame>.git
                process = subprocess.Popen(['git', 'remote', 'add', "origin", "git@github.com:" + self.git + "/" + cname + ".git"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process.wait()
                process = subprocess.Popen(['git', 'push', '-u', 'origin','master'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                process.wait()
    
    #update API and Github
    def update(self):
        data = {
            "url": self.url,
            "first_name": self.first_name,
            "last_name": self.first_name,
            "classes": self.classes,
            "git": self.git,
            "ion_user": self.username
        },
        r = requests.put(url = self.url, data= data, headers={'Content-type': 'application/json'} ,auth=('raffukhondaker','hackgroup1'))

    def command(self, command):
        ar = []
        command = command.split(" ")
        for c in command:
            ar.append(c)
        process = subprocess.Popen(ar, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        process.wait()


    #class name format: <course-name>_<ion_user>

    #turn existing directory into class
    def addClas(self, path):
        cname = path.split("/")
        if(os.path.exists(cname)):
            print("Already synced to: " + str(self.username))
            return


    #make a new class from scratch
    def makeClass(self, subject):
        cname = subject + "_" + self.username
        os.chdir(self.username)
        #check if class exists
        if(os.path.exists(cname)):
            print("Already synced to: " + str(self.username))
            return
        else:
            os.mkdir(cname)
            f=open(cname + "/README.md", "w")
            f.close()
            #push to remote repo
            os.chdir(cname)
            command(self, 'git init')
            command(self, 'git add .')
            command(self, 'git commit -m "Hello Class!"')
            #git remote add origin git@github.com:alexpchin/<reponame>.git
            command(self, 'git remote add origin git@github.com:'+ self.git + "/" + cname + ".git")
            command(self, 'git push -u origin master')

            cinfo=[
            {
                "name":subject,
                "assignments":[],
                "repo": "https://github.com:" + self.git + "/" + cname + ".git",
                "default_file": [
                    {
                        "name":"README.md"
                    }
                ]
            }
            ]

            #update  rest API
            self.classes.append(cinfo)
            update(self)

    def addAsignment(self, class_name, name):
        os.chdir(self.username+"/")

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

def updateAssignment(name):
    print(name)

def comment(filename, text):
    print(text)


