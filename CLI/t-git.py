import subprocess
import os
import requests
import webbrowser

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

    def command(self,command):
        ar = []
        command = command.split(" ")
        for c in command:
            ar.append(c)
        process = subprocess.Popen(ar, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p=process.poll()
        output = process.communicate()[0]
        print(output.decode('utf-8'))

    def initTeacher(self):
        if(os.path.exists(self.username )):
            print("Already synced to: " + str(self.username))
            return
        os.mkdir(self.username)
        classes = self.classes
        # make classes directory
        for c in classes:
            cname= c['name']
            cpath = self.username + "/" + cname

            input("Make new Git Repo with name: "  + cname + " (Press  any key to continue)\n")
            webbrowser.open('https://github.com/new')
            input("Repo created? (Press any key to continue)\n")

            url='https://github.com/' + self.git + "/" + cname
            print(url)
            while(requests.get(url).status_code  != 200):
                print(requests.get(url))
                r = input("Repo not created yet. (Press any key to continue after repo created, or 'N' to exit)\n")
                if(r=="N" or r=="No"):
                    return
            cdir = os.getcwd()
            os.chdir(self.username)
            self.command('git clone ' + url)
            os.chdir(cdir)

            #make class directory
            #make default files for each class
            for filename in c['default_file']:
                f=open(cpath+"/"+filename['name'], "w")
                f.close()
            
            #make assignments directory
            for a in c['assignments']:
                path = cpath + "/" + a['name']
                if(os.path.exists(path)):
                    print(path + " already exists...")
                else:
                    os.mkdir(path)
                    f=open(path + "/instructions.txt", "w")
                    f.close()

            #push to remote repo
            os.chdir(cpath)
            print(cpath)
            self.command('git add .')
            self.command('git commit -m Hello_Class')
            self.command('git push -u origin master')
                
    
    #update API and Github, all  assignments / classes
    def update(self):
        #lists all classes
        classes = os.listdir(self.username)

        #checks all class directories first
        for c in classes:
            if(checkClass(self, c) == False):
                return
        cdict = []
        for c in classes:
            #lists all assignments and default files
            ass =  os.listdir(c)
            #if  no  .git, directory not synced to  git  or  API
            if '.git' in ass == False:
                addClass(self, c)
            else:
                #push to git
                loc = os.getcwd()
                os.chdir(c)
                command(self, 'git init')
                command(self, 'git add .')
                command(self, 'git commit -m "Update"')
                command(self, 'git push -u origin master')
                os.chdir(loc)
            #assignments
            adict = []
            #default  files for classes
            fdict=[]
            #default files  for assignments
            afdict=[]
            for a in ass:
                aname=a
                #need to add  option
                due_date="2020-06-07T07:46:30.537197Z",
                if(os.path.isfile(a)):
                    fdict.append({
                        'name':a
                    })
                elif(os.path.isdir(a)):
                    for af in  a:
                        if(os.path.isfile(af)):
                            afdict.append({
                                'name':af
                            })
                    adict.append({
                        'name':aname,
                        'due_date':due_date,
                        'files':fdict
                    })

            cdict.append({
                'name':c,
                'repo': 'https://github.com:"' + self.git + "/" + c + ".git",
                'assignments':adict,
                'default_file':fdict
            })
        r = requests.put(url = self.url, data= cdict, headers={'Content-type': 'application/json'} ,auth=('raffukhondaker','hackgroup1'))

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
                count=count+1
            if(os.path.isdir(d)):
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

        if(count == 0):
            print("Need a default file in the " + path + " Directory!")
            return  False
        return True

    def addClass(self, path):
        cname = path.split("/")
        cname = cname[len(cname)-1]
        #push to remote repo
        if(os.path.exists(path)):
            print("Already synced")
            return 
        if(checkClass(self, path)):
            os.chdir(cname)
            command(self, 'git init')
            command(self, 'git add .')
            command(self, 'git commit -m "Hello Class!"')
            #git remote add origin git@github.com:alexpchin/<reponame>.git
            command(self, 'git remote add origin git@github.com:'+ self.git + "/" + cname + ".git")
            command(self, 'git push -u origin master')


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
                "name":cname,
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
            data = {
                "url": self.url,
                "first_name": self.first_name,
                "last_name": self.first_name,
                "classes": self.classes,
                "git": self.git,
                "ion_user": self.username
            },
            r = requests.put(url = self.url, data= data, headers={'Content-type': 'application/json'} ,auth=('raffukhondaker','hackgroup1'))

#make student repo by student id
    def addStudent(self,stid):
        print(stid)

    def comment(self):
        print("heheheh")

data = getData("eharris1")
print(data)
t = Teacher(data)
t.initTeacher()


