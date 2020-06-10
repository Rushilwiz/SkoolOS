import subprocess
import os
import requests
import webbrowser
import pprint
import json

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

class Teacher:
    def __init__(self, data):
        # teacher info already  stored in API
        # intitialze fields after GET request
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.git=data['git']
        self.username=data['ion_user']
        self.url= "http://127.0.0.1:8000/teachers/" + self.username + "/"
        
        classes=data['classes'].split(",")
        cdict = []
        for cid in classes:
            adict=[]
            c = getDB("http://127.0.0.1:8000/classes/" + cid + "/")
            name=c['name']
            repo=c['repo']
            path=c['path']
            teacher=c['teacher']
            id=c['id']
            assignments=c['assignments'].split(",")
            dfs = c['default_file'].split(' ')
            dfdict=[]
            for fid in dfs:
                f =  getDB("http://127.0.0.1:8000/files/" + fid + "/")
                fname=f['name']
                fpath=f['path']
                dfdict.append({
                    'name':fname,
                    'path':fpath,
                    'classes':classes,
                    'assignment':"none",
                    'id':fid,
                })    
            for aid in assignments:
                fdict=[]
                a = getDB("http://127.0.0.1:8000/assignments/" + aid + "/")
                aname= a['name']
                due_date = a['due_date']
                apath=a['path']
                classes=a['classes']
                files = a['files'].split(' ')
                for fid in files:
                    f =  getDB("http://127.0.0.1:8000/files/" + fid + "/")
                    fname=f['name']
                    fpath=f['path']
                    fdict.append({
                        'name':fname,
                        'path':fpath,
                        'classes':classes,
                        'assignment':aname,
                        'id':fid,
                    })
                adict.append({
                    'name':aname,
                    'due_date':due_date,
                    'path':apath,
                    'classes':classes,
                    'teacher':teacher,
                    'files':fdict,
                })
            cdict.append({
                'name':name,
                'path':path,
                'teacher':teacher,
                'assignments':adict,
                'default_file':adict,
            })
            
        self.classes = cdict

    def command(self,command):
        ar = []
        command = command.split(" ")
        for c in command:
            ar.append(c)
        process = subprocess.Popen(ar, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        p=process.poll()
        output = process.communicate()[0]
        #print(output.decode('utf-8'))

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
                
    def checkGit(self, ass):
        for a in ass:
            if a =='.git':
                return True
        return False

    def compareDB(self, fdict, url):
        URL = url
        r = requests.get(url = URL, auth=('raffukhondaker','hackgroup1')) 
        data = r.json()['results']
        allfiles = data
        # far = []
        # for f in allfiles:
        #     far.append(f['path'])

        for f in  fdict:
            URL = url
            in_db = False
            pid=None
            for dbf in allfiles:
                if(dbf['path'] == f['path']):
                    in_db=True
                    break
            if(in_db==False):
                r = requests.post(url = URL, data=f , auth=('raffukhondaker','hackgroup1')) 
                print("POST: (" + URL  + "): " + f['path'])
                f['url']=r.json()['url']
                print(r.status_code)
            else:
                URL = URL + str(dbf['id']) + "/"
                r = requests.put(url = URL, data=f , auth=('raffukhondaker','hackgroup1')) 
                print(r.status_code)
                print("UPDATED: (" + URL  + "): " + f['path'])
                f['url']=r.json()['url']
                f['id']=dbf['id']
                print(f)

        return fdict

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
                self.addClass(path)
            else:
                #push to git
                loc = os.getcwd()
                os.chdir(path)
                self.command('git add .')
                self.command('git commit -m "Update"')
                self.command('git push -u origin master')
                os.chdir(loc)
                ass.remove('.git')

            loc = os.getcwd()
            os.chdir(path)
            repo = self.command('git config --get remote.origin.url')
            os.chdir(loc)

            #assignments
            adict = []
            #default  files for classes
            fdict=[]
            #default files  for assignments
            afdict=[]
            for a in ass:
                aname=a
                path = self.username  +  "/" + c + "/" + a
                #need to add  option
                due_date= '2020-06-07T07:46:30.537197Z',
                #check for default file
                if(os.path.isfile(path)):
                    fdict.append({
                        'name':a,
                        'path':path
                    })
                elif(os.path.isdir(path)):
                    for af in os.listdir(path):
                        path =  path+ "/" + af
                        if(os.path.isfile(path)):
                            afdict.append({
                                'name':af,
                                'path':path
                            })
                    path = self.username  +  "/" + c + "/" + a
                    adict.append({
                        'name':aname,
                        'due_date': due_date[0],
                        'path':path,
                        'files':afdict
                    })

                fdict=self.compareDB(fdict, "http://127.0.0.1:8000/files/")
                afdict=self.compareDB(afdict,"http://127.0.0.1:8000/files/")
                
            adict=self.compareDB(adict, 'http://127.0.0.1:8000/assignments/')

            path = self.username  +  "/" + c
            cdict.append({
                'name':c,
                'repo': repo,
                'path':path,
                'assignments':adict,
                'default_file':fdict,
            })
        cdict=self.compareDB(cdict,'http://127.0.0.1:8000/classes/')

        mdict= {
            'first_name':self.first_name,
            'last_name':self.last_name,
            'git':self.git,
            'ion_user':self.username,
            'classes':cdict,
        }

        data = json.dumps(mdict)
        # r = requests.put(url = 'http://127.0.0.1:8000/teachers/eharris1/', data=data, headers={'Content-type': 'application/json'} ,  auth=('raffukhondaker','hackgroup1'))
        # print(print(r.json()))


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

        if(deffile):
            print("Need a default file in the " + path + " Directory!")
            return  False
        return True

    #adds class to  git,  not API
    def addClasstoGit(self, path):
        cname = path.split("/")
        cname = cname[len(cname)-1]
        #push to remote repo
        if(self.checkClass(path)):
            input("Make new Git Repo with name: "  + cname + " (Press  any key to continue)\n")
            webbrowser.open('https://github.com/new')
            input("Repo created? (Press any key to continue)\n")

            url='https://github.com/' + self.git + "/" + cname
            print(url)
            while(requests.get(url).status_code  != 200):
                print(requests.get(url))
                r = input("Repo not created yet. (Press any key to continue after repo created, or 'N' to exit)\n")
                if(r=="N" or r=="No"):
                    return None
            cdir = os.getcwd()
            os.chdir(path)
            self.command('git init')
            self.command('git add .')
            self.command('git commit -m Hello_Class')
            self.command('git remote add origin ' + url + '.git')
            self.command('git push -u origin master')
            os.chdir(cdir)


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

# data = getData("eharris1")
data={'url': 'http://127.0.0.1:8000/teachers/eharris1/', 'first_name': 'Errin', 'last_name': 'Harris', 'git': 'therealraffi', 'ion_user': 'eharris1', 'classes': [{'url': 'http://127.0.0.1:8000/classes/1/', 'name': 'Math5_eharris1', 'repo': 'http://127.0.0.1:8000/assignments/3/', 'assignments': [{'name': 'Week1_HW', 'due_date': '2020-06-07T07:46:30.537197Z', 'url': 'http://127.0.0.1:8000/assignments/1/', 'files': [{'name': 'instructions.txt'}]}, {'name': 'Week2_HW', 'due_date': '2020-06-07T07:46:30.548596Z', 'url': 'http://127.0.0.1:8000/assignments/2/', 'files': [{'name': 'instructions.txt'}]}], 'default_file': [{'name': 'instructions.txt'}]}]}
t = Teacher(data)
t.update()


