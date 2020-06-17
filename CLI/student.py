import subprocess
import os
import requests
import webbrowser
import pprint
import json
import shutil
import time
import pyperclip
import datetime


# git clone student directory ==> <student-id>/classes/assignments

# get teacher info from api
def getStudent(ion_user, password):
    URL = "http://127.0.0.1:8000/api/students/" + ion_user + "/"
    r = requests.get(url=URL, auth=(ion_user, password))
    if (r.status_code == 200):
        data = r.json()
        return data
    elif (r.status_code == 404):
        return None
        print("Make new account!")
    elif (r.status_code == 403):
        return None
        print("Invalid username/password")
    else:
        return None
        print(r.status_code)

#makes a GET request to given url, returns dict
def getDB(user, pwd, url):
    """
    Sends a GET request to url
    param user: username
    param pwd: password
    param url: URL for request
    return: json request response
    """
    r = requests.get(url=url, auth=(user, pwd))
    print("GET:" + str(r.status_code))
    return(r.json())

#makes a PATCH (updates instance) request to given url, returns dict
def patchDB(user, pwd, data, url):
    """
    Sends a PATCH request to url
    param user: username
    param pwd: password
    param url: URL for request
    param data: data to request
    return: json request response
    """
    r = requests.patch(url=url, data=data, auth=(user, pwd))
    print("PATCH:" + str(r.status_code))
    return r.json()


#makes a POST (makes new instance) request to given url, returns dict
def postDB(user, pwd, data, url):
    """
    Sends a POST request to url
    param user: username
    param pwd: password
    param url: URL for request
    param data: data to request
    return: json request response
    """
    r = requests.post(url=url, data=data, auth=(user, pwd))
    print("POST:" + str(r.status_code))
    return r.json()


#makes a PUT (overwrites instance) request to given url, returns dict
def putDB(user, pwd, data, url):
    """
    Sends a PUT request to url
    param user: username
    param pwd: password
    param url: URL for request
    param data: data to request
    return: json request response
    """
    r = requests.put(url=url, data=data, auth=(user, pwd))
    print("PUT:" + str(r.status_code))
    return r.json()


#makes a DELETE (delete instance) request to given url, returns dict
def delDB(user, pwd, url):
    """
    Sends a DELETE request to url
    param user: username
    param pwd: password
    param url: URL for request
    return: json request response
    """
    r = requests.delete(url=url, auth=(user, pwd))
    print("DELETE:" + str(r.status_code))
    return None


def command(command):
    ar = []
    command = command.split(" ")
    for c in command:
        ar.append(c)
    process = subprocess.Popen(ar, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = process.poll()
    output = process.communicate()[0]
    print(output.decode('utf-8'))
    return output.decode('utf-8')


####################################################################################################################################

# public methods: deleteClass, makeClass, update
class Student:
    def __init__(self, data, password):
        # teacher info already  stored in API
        # intitialze fields after GET request
        self.git = data['git']
        self.username = data['ion_user']
        self.url = "http://127.0.0.1:8000/api/students/" + self.username + "/"
        self.grade = data['grade']
        self.completed = data['completed']
        self.user = data['user']
        self.password = password
        self.completed = data['completed']
        # classes in id form (Example: 4,5)
        # storing  actual classes
        cid = data['classes'].split(",")
        try:
            cid.remove('')
        except:
            pass
        try:
            cid.remove("")
        except:
            pass
        classes = []
        for c in cid:
            url = "http://127.0.0.1:8000/api/classes/" + str(c) + "/"
            classes.append(getDB(self.username, self.password,url))

        self.classes = classes
        self.sclass = str(data['classes'])

        # storing  added_to classes
        nid = data['added_to'].split(",")
        try:
            nid.remove('')
        except:
            pass
        try:
            nid.remove("")
        except:
            pass
        nclasses = []
        for c in nid:
            url = "http://127.0.0.1:8000/api/classes/" + str(c) + "/"
            nclasses.append(getDB(self.username, self.password,url))

        self.new = nclasses
        self.snew = str(data['added_to'])
        self.repo = data['repo']

        if (os.path.isdir(self.username) == False):
            if (self.repo == ""):
                user = self.git
                pwd = input("Enter Github password: ")
                # curl -i -u USER:PASSWORD -d '{"name":"REPO"}' https://api.github.com/user/repos
                url = "curl -i -u " + user + ":" + pwd + " -d '" + '{"name":"' + self.username + '"}' + "' " + "https://api.github.com/user/repos"
                print(url)
                os.system(url)
            cdir = os.getcwd()
            command('git clone https://github.com/' + self.git + '/' + self.username + '.git')
            os.chdir(self.username)
            command('git checkout master')
            command('touch README.md')
            command('git add README.md')
            command('git commit -m "Hello"')
            command('git push -u origin master')
            os.chdir(cdir)
            self.repo = 'https://github.com/' + self.git + '/' + self.username + '.git'
            data = {
                'repo': self.repo
            }
            print(patchDB(self.username, self.password,data, self.url))
        print("Synced to " + self.username)

    def getClasses(self):
        classes = self.classes
        for c in classes:
            print(c['name'])

    def getAssignments(self, course, span):
        span = datetime.timedelta(span, 0)
        classes = self.classes
        for c in classes:
            print(c['name'])
            alist = c['assignments']
            for a in alist:
                ass = getDB(self.username, self.password,"http://127.0.0.1:8000/api/assignments/" + a)
                now = datetime.datetime.now()
                try:
                    due = ass['due_date'].replace("T", " ").replace("Z", "")
                    due = datetime.datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
                    diff = now - due
                    zero = datetime.timedelta(0, 0)
                    # check due ddate is in span range is now past date (- timdelta)
                    if (diff < span and diff > zero):
                        print(a + " due in:" + str(now - due))

                except Exception as e:
                    print(e)
                    pass

    # update API and Github, all  assignments / classes
    def update(self):
        cdir = os.getcwd()
        os.chdir(self.username)
        command("git checkout master")
        for c in self.classes:
            print("UPDATING CLASS: " + str(c['name']))
            data = getDB(self.username, self.password,"http://127.0.0.1:8000/api/classes/" + str(c['name']))
            # command("git checkout master")
            command("git checkout " + data['name'])
            command("git add .")
            command("git commit -m " + data['name'])
            command("git pull origin " + data['name'])
            command("git push -u origin " + data['name'])
            command("git checkout master")
        os.chdir(cdir)
        for c in self.new:
            print("ADDING CLASS: " + str(c['name']))
            self.addClass(str(c['name']))
        command("git checkout master")
        print(os.getcwd())

    # updates 1 class, does not switch to master
    def updateClass(self, course):
        if ((course in self.sclass) == False):
            print("Class not found")
            return
        cdir = os.getcwd()
        os.chdir(self.username)
        command("git checkout " + course)
        command("git add .")
        command("git commit -m " + course)
        command("git pull origin " + course)
        command("git push -u origin " + course)

    # class name format: <course-name>_<ion_user>

    # add  classes from 'new' field
    def addClass(self, cid):

        data = getDB(self.username, self.password,'http://127.0.0.1:8000/api/classes/' + str(cid))
        if ((cid in self.snew) == False or (self.username in data['confirmed'])):
            print("Already enrolled in this class.")
            return None
        if ((cid in self.sclass) or (self.username in data['unconfirmed']) == False):
            print("Not added by teacher yet.")
            return None

        # add class teacher as cocllaborator to student repo
        print(os.getcwd())
        pwd = input("Enter Github password: ")
        tgit = getDB(self.username, self.password,"http://127.0.0.1:8000/api/teachers/" + data['teacher'] + "/")['git']
        url = "curl -i -u " + self.git + ":" + pwd + " -X PUT -d '' " + "'https://api.github.com/repos/" + self.git + "/" + self.username + "/collaborators/" + tgit + "'"
        print(url)
        os.system(url)

        cdir = os.getcwd()
        os.chdir(self.username)
        # path1 = self.username + "/" + self.username
        # path2 = self.username
        # if(os.path.isdir(path1)):
        #     os.chdir(path1)
        # else:
        #     os.chdir(self.username)
        #     command("git clone " + self.repo)
        #     os.chdir(self.username)

        # push to git, start at master
        #os.chdir(self.username)
        command("git checkout master")
        command("git branch " + data['name'])
        command("git commit -m initial")
        command("git push origin " + data['name'])
        command("git checkout master")
        # git clone --single-branch --branch <branchname> <remote-repo>
        os.chdir(cdir)

        # data['unconfirmed'] = data['unconfirmed'].replace("," + self.username, "")
        # data['unconfirmed'] = data['unconfirmed'].replace(self.username, "")
        # data['confirmed'] = data['confirmed'] + "," + self.username
        # if(data['confirmed'][0] == ','):
        #     data['confirmed'] = data['confirmed'][1:]
        #     print(data['confirmed'])
        # print(putDB(data, 'http://127.0.0.1:8000/api/classes/'+ str(cid) + "/"))

        # add teacher as collaborator
        # curl -i -u "USER:PASSWORDD" -X PUT -d '' 'https://api.github.com/repos/USER/REPO/collaborators/COLLABORATOR'
        user = self.git

        self.classes.append(data)
        if (len(self.sclass) == 0):
            self.sclass = data['name']
        else:
            self.sclass = self.sclass + "," + str(data['name'])

        # upddate self.new
        snew = ""
        new = []
        for i in range(len(self.new)):
            if (self.new[i]['name'] == data['name']):
                del self.new[i]
                # recreate sclass field, using ids
                for c in self.new:
                    snew = snew + str(c['name']) + ","
                    new.append(getDB(self.username, self.password,"http://127.0.0.1:8000/api/classes/" + str(cid)))
                self.snew = snew
                self.new = new
                break

        # update teacher instance in db, classes field
        data = {
            'user': self.user,
            'added_to': self.snew,
            'classes': self.sclass
        }
        print(self.url)
        print(patchDB(self.username, self.password,data, self.url))
        return data

    def submit(self, path):
        # 2022rkhondak/English11_eharris1/Essay1
        # check if valid assignment
        parts = path.split("/")
        if (len(parts) != 3):
            print("Assignment path too short")
            return
        isclass = False
        for c in self.classes:
            if (c['name'] == parts[1]):
                isclass == True
                break
        if (parts[0] != self.username and isclass and os.path.isdir(path) == False):
            print("Not valid assignment")
            return
        if ((parts[1] + "/" + parts[2]) in self.completed):
            print(parts[2] + " already submited. ")
            # return
        resp = input("Are you sure you want to submit? You cannot do this again.(y/N) ")
        if (resp == 'y'):
            os.chdir(self.username + "/" + parts[1])
            command("git add .")
            command("git commit -m submit")
            command("git tag " + parts[1] + "-final")
            command("git push -u origin " + self.username + " --tags")
            self.completed = self.completed + "," + parts[1] + "/" + parts[2]
            data = {
                'user': self.user,
                'git': self.git,
                'ion_user': self.username,
                'student_id': self.student_id,
                'added_to': self.snew,
                'url': self.url,
                'classes': self.sclass,
                'grade': self.grade,
                'completed': self.completed
            }
            # print(putDB(data, "http://127.0.0.1:8000/api/students/" + self.username + "/"))

    def viewClass(self, courses):
        self.update()
        cdir = os.getcwd()
        os.chdir(self.username)
        for c in self.classes:
            if c['name'] == courses:
                command("git checkout " + courses)
                print(os.listdir())
                os.chdir(cdir)
                return
        os.chdir(cdir)
        print("Class not found")
        return

    def exitCLI(self):
        print(os.getcwd())
        self.update()
        command("git checkout master")

    def submit(self, course, assignment):
        cdir = os.getcwd()
        os.chdir(self.username)
        print(os.getcwd())
        command("git add .")
        command("git commit -m update")
        command('git checkout ' + course)
        ass = os.listdir()
        oname = ''
        inclass = False
        for a in ass:
            if a in assignment:
                inclass = True
                oname = a + "_" + course
                break
        if (inclass == False):
            print(assignment + " not an assignment of " + course)
            command('git checkout master')
            os.chdir(cdir)
            return

        command('touch ' + assignment + '/SUBMISSION')
        command("git add .")
        command("git commit -m submit")
        command("git tag " + assignment + "-final")
        command("git push -u origin " + course + " --tags")
        command('git checkout master')
        self.completed = assignment + "," + self.completed
        data = {
            'completed': self.completed
        }
        patchDB(self.username, self.password, data, self.url)
        os.chdir(cdir)


#data = getStudent("2022rkhondak", "PWD")
#s = Student(data, "PWD")
# s.viewClass("APLit_eharris1")
# #s.addClass("APLit_eharris1")
# # #s.update()
# s.exitCLI()

def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
