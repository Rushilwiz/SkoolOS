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


# from django.conf import settings
# import django

# from Website.config.settings import DATABASES, INSTALLED_APPS
# INSTALLED_APPS.remove('users.apps.UsersConfig')
# INSTALLED_APPS.remove('api')
# INSTALLED_APPS.remove('skoolos.apps.SkoolosConfig')
# INSTALLED_APPS.append('Website.api')
# settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS)
# django.setup()

# from ..Website.api.models import *
# git clone student directory ==> <student-id>/classes/assignments

# get teacher info from api
def getTeacher(ion_user, password):
    """
    Gets information about a teacher from the api
    :param ion_user: a teacher
    :param password: the teacher's password
    :return: teacher information or error
    """
    URL = "http://127.0.0.1:8000/api/teachers/" + ion_user + "/"
    r = requests.get(url=URL, auth=(ion_user,password))
    print(r.json())
    if r.status_code == 200:
        data = r.json()
        return data
    elif r.status_code == 404:
        return None
        print("Make new account!")
    elif r.status_code == 403:
        return None
        print("Invalid username/password")
    else:
        return None
        print(r.status_code)

#makes a GET request to given url, returns dict
def getDB(user, pwd, url):
    """
    Sends a GET request to url
    :param user: username
    :param pwd: password
    :param url: URL for request
    :return: json request response
    """
    r = requests.get(url=url, auth=(user, pwd))
    print("GET:" + str(r.status_code))
    return(r.json())

#makes a PATCH (updates instance) request to given url, returns dict
def patchDB(user, pwd, data, url):
    """
    Sends a PATCH request to url
    :param user: username
    :param pwd: password
    :param url: URL for request
    :param data: data to request
    :return: json request response
    """
    r = requests.patch(url=url, data=data, auth=(user, pwd))
    print("PATCH:" + str(r.status_code))
    return r.json()


#makes a POST (makes new instance) request to given url, returns dict
def postDB(user, pwd, data, url):
    """
    Sends a POST request to url
    :param user: username
    :param pwd: password
    :param url: URL for request
    :param data: data to request
    :return: json request response
    """
    r = requests.post(url=url, data=data, auth=(user, pwd))
    print("POST:" + str(r.status_code))
    return r.json()


#makes a PUT (overwrites instance) request to given url, returns dict
def putDB(user, pwd, data, url):
    """
    Sends a PUT request to url
    :param user: username
    :param pwd: password
    :param url: URL for request
    :param data: data to request
    :return: json request response
   """
    r = requests.put(url=url, data=data, auth=(user, pwd))
    print("PUT:" + str(r.status_code))
    return r.json()


#makes a DELETE (delete instance) request to given url, returns dict
def delDB(user, pwd, url):
    """
    Sends a DELETE request to url
    :param user: username
    :param pwd: password
    :param url: URL for request
    :return: json request response
    """
    r = requests.delete(url=url, auth=(user, pwd))
    print("DELETE:" + str(r.status_code))
    return None


def command(command):
    """
    Runs a shell command
    :param command: shell command
    """
    ar = []
    command = command.split(" ")
    for c in command:
        ar.append(c)
    process = subprocess.Popen(ar, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = process.poll()
    output = process.communicate()[1]
    # print(output.decode('utf-8'))


####################################################################################################################################

# public methods: deleteClass, makeClass, update
class Teacher:
    def __init__(self, data, password):
        # teacher info already  stored in API
        # intitialze fields after GET request
        """
        Initializes a Teacher with the data from the api
        :param data: api data
        """
        self.git = data['git']
        self.username = data['ion_user']
        self.url = "http://127.0.0.1:8000/api/teachers/" + self.username + "/"
        self.id = data['user']
        self.password = password
        # classes in id form (Example: 4,5)

        # array
        self.classes = data['classes']
        if os.path.isdir(self.username + "/Students"):
            print("Synced to " + self.username)
            existing_classes = os.listdir(self.username)
            for  c in self.classes:
                if not c in str(existing_classes):
                    os.mkdir(self.username + "/" + c)
                    print("Updated: " + c)
                    command("touch " + self.username + "/" + c + "/README.md")
                    os.makedirs(self.username + "/Students/" + c)

        else:
            os.makedirs(self.username + "/Students")

        # 2020-05-11 12:25:00

    # class name format: <course-name>_<ion_user>

    # turn existing directory into class, Pre-condition: directory exists
    # relative path to  class: 2022rkhondak/Math4
    def checkClass(self, path):
        """
        Checks if a directory is valid for creating a class
        :param path: path to the new class directory
        """
        cname = path.split("/")
        cname = cname[len(cname) - 1]
        if os.path.isfile(path):
            print(path + " must be in a Class directory.")
            return False
        if not (("_" + self.username) in cname):
            print(
                "Incorrect class name: Must be in the format: " + self.username + "/<course-name>_<ion_user>, not " + path)
            return False
        dirs = os.listdir(path)
        # checks if there  is a file (not within Assignments) in class, need at least 1
        deffile = False
        # checks if there  is a file in an Assignment, need at least 1 (default True  in case no  assignments)
        as_file = True
        as_bad = ""

        for d in dirs:
            if os.path.isfile(d):
                deffile = True
            else:
                # checks if there  is a file in an Assignment, need at least 1
                as_file = False
                asdir = os.listdir(path + "/" + d)
                for a in asdir:
                    if os.path.isfile(path + "/" + d + "/" + a):
                        as_file = True
                if not as_file:
                    as_bad = d
                    break
        if not as_file:
            print("Assignment '" + as_bad + "' does  not  have a default file!")
            return False

        if not deffile:
            print("Need a default file in the " + path + " Directory!")
            return False
        return True

    def checkInDB(self, path):
        """
        Checks if "path" is in the database
        :param path: path to directory
        """
        n = path.split("/")
        n = n[len(n) - 1]
        for c in self.classes:
            if n == c['name']:
                return True
        return False

    # make class from existing directory, add to git and api
    def addClass(self, path):
        """
        Creates a class from an existing directory, adding it to the proper git repository and the api
        :param path:
        """
        cname = path.split("/")
        cname = cname[len(cname) - 1]
        for c in self.classes:
            if c == cname:
                print(cname + " already exists.")
                return
        if self.checkClass(path):
            cpath = self.username + "/" + cname
            subject = cname.split("_")[0]
            period = int(input("Enter period: "))
            while(not (type(period) is int and period >= 0)):
                print("Incorrect format")
                period = int(input("Enter period: "))
            data = {
                "name": cname,
                "repo": "",
                "path": cpath,
                "subject": subject,
                "period":period,
                "teacher": self.username,
                "owner": self.id
            }
            # make class instance in db
            postDB(self.username, self.password, data, 'http://127.0.0.1:8000/api/classes/')
            time.sleep(1)
            self.classes.append(cname)
            # add to  instance
            # update  self.classes
            data = {
                'classes': self.classes
            }
            print(self.classes)
            print(patchDB(self.username, self.password, data, 'http://127.0.0.1:8000/api/teachers/' + self.username + "/"))

    # make a new class from scratch
    # subject: string, assignments: list
    # class name must be: <subject>_<ion_user>
    def makeClass(self, cname):
        """
        Makes a class with its own new directory
        :param cname: name of class
        """
        # check if class exists
        path = self.username + "/" + cname
        isclass = False
        acourses = getDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/")['results']
        for c in acourses:
            if c['name'] == cname:
                isclass = True
                break
        if os.path.exists(path) or isclass:
            print("Class already exists: " + cname)
            if isclass:
                print("Class already exists in Database")
            return
        else:
            if not (("_" + self.username) in cname):
                print("class name must be: " + cname + "_" + self.username)
                return
            cdir = os.getcwd()
            os.mkdir(path)
            f = open(path + "/README.md", "w")
            f.close()
            os.makedirs(self.username + "/Students/" + cname)
            # push to remote repo
            # os.chdir(path)
            # for a in assignments:

            #     os.mkdir(a)
            #     f=open(a + "/instructions.txt", "w")
            #     f.close()
            # os.chdir(cdir)

            self.addClass(path)

    def deleteClass(self, path):
        """
        Deletes an existing class
        :param path: class directory path
        """
        if not os.path.exists(path):
            print(path + " does not exist locally.")
        resp = input("Do you want to delete " + path + " from the SkoolOS system? (y/N) ")
        if resp != 'y':
            return

        cname = path.split("/")
        cname = cname[len(cname) - 1]
        repo = ''
        print("DELETE: " + self.classes[i]['name'])
        for i in range(len(self.classes)):
            c = self.classes[i]
            if c == cname:
                del self.classes[i]
                # data={
                #     'classes':self.classes,
                # }
                # print(patchDB(data, self.url))
                delDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/" + cname + "/")
                break

        # remove locally
        try:
            shutil.rmtree(path)
        except:
            pass

        # remove from student directories

    def isStudent(self, student):
        """
        Checks if the student exists
        :param student: a student
        :return: True if student exists, False otherwise
        """
        r = requests.get(url="http://127.0.0.1:8000/api/students/" + student + "/",
                         auth=(self.username, self.password))
        if r.status_code != 200:
            return False
        return True

    def reqStudent(self, sname, cname):
        """
        Request student informatiion from the api
        :param sname: student's name
        :param cname: class name
        :return: True if successful
        """
        if not self.isStudent(sname):
            print(sname + " does not exist.")
            return False
        course = getDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/" + cname)
        if sname in str(course['unconfirmed']):
            print(sname + " already requested.")
            return True
        if sname in str(course['confirmed']):
            print(sname + " already enrolled.")
            return False

        student = getDB(self.username, self.password, "http://127.0.0.1:8000/api/students/" + sname)
        try:
            if student['added_to'] == "":
                student['added_to'] = course['name']
            else:
                student['added_to'] = student['added_to'] + "," + course['name']
        except:
            print(sname + " does not exist.")
            return False
        print(student['added_to'])
        data = {
            'added_to': student['added_to'],
        }
        student = patchDB(self.username, self.password, data, "http://localhost:8000/api/students/" + student['ion_user'] + "/")
        student = getDB(self.username, self.password, "http://localhost:8000/api/students/" + sname + "/")
        if not course['unconfirmed']:
            course['unconfirmed'] = student['ion_user']
        else:
            course['unconfirmed'] = course['unconfirmed'].append(student['ion_user'])
        cinfo = {
            "unconfirmed": course['unconfirmed']
        }
        print(cinfo)
        patchDB(self.username, self.password, cinfo, "http://localhost:8000/api/classes/" + course['name'] + "/")
        return True

    # Student should have confirmed on their endd, but class had not been updated yet
    # git clone confirmed student repo, copy files into repo and push branch
    def addStudent(self, sname, cname):
        """
        Adds a student to a class
        :param sname: student name
        :param cname: class name
        :return:
        """
        if not self.isStudent(sname):
            print(sname + " does not exist.")
            return False

        student = getDB(self.username, self.password, "http://127.0.0.1:8000/api/students/" + sname)
        course = getDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/" + cname)

        if (os.path.exists(self.username + "/Students/" + cname + "/" + student['ion_user']) or (
                student['ion_user'] in course['confirmed']) == True):
            print(student['ion_user'] + " already added to class")
            return True
        if (cname in student['added_to']) or not (cname in student['classes']):
            print(student['ion_user'] + " has not confirmed class yet")
            return False
        if not (student['ion_user'] in course['unconfirmed']):
            print(course['unconfirmed'])
            print(student['ion_user'] + " has not been requested to join yet.")
            return False

        # git clone and make student/class directories
        cdir = os.getcwd()
        cpath = self.username + "/" + cname
        path = self.username + "/Students/" + cname
        spath = self.username + "/Students/" + cname + "/" + student['ion_user']
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.path.isdir(spath):
            os.chdir(path)
            command("git clone " + student['repo'])
            os.chdir(cdir)

        # push to git
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

        if not course['confirmed']:
            course['confirmed'] = student['ion_user']
        else:
            course['confirmed'].append(student['ion_user'])

        # only 1 pereson on confirmeed
        if len(course['unconfirmed']) == 1:
            course['unconfirmed'] = []
        # mutiple
        else:
            course['unconfirmed'].remove(student['ion_user'])

        cinfo = {
            "confirmed": course["confirmed"],
            "unconfirmed": course['unconfirmed']
        }
        print(putDB(self.username, self.password, course, "http://localhost:8000/api/classes/" + course['name'] + "/"))
        return True

    # goes through list of studennts, tries to add, then request, return unconfirmed students
    def reqAddStudentList(self, array, cname):
        """
        Runs addStudent() on all students in array
        :param array: an array of students
        :param cname: class name
        :return: students that have not confirmed the request
        """
        unconf = []
        for i in range(len(array)):
            a = array[i]
            if not self.addStudent(a, cname):
                self.reqStudent(a, cname)
                unconf.append(a)
        return unconf

    # add local path to student directory, make new instance in api
    def addAssignment(self, path, course, due):
        """
        Creates an assignment for "course" that is  due on "due"
        :param path: directory of assignment
        :param course: course name
        :param due: due date
        :return: False if unsuccessful
        """
        parts = path.split("/")
        aname = parts[len(parts) - 1]
        oname = aname + "_" + course

        if (os.path.isdir(path) == 0 or len(parts) < 3) or aname in str(self.classes):
            print("Not valid path.")
            return False
        if not (parts[1] in str(self.classes)):
            print("Not in valid class directory")
            return False
        # parts of assignment name (Essay1, APLit)
        # if((course in aname) == False):
        #     print("Assignment named incorrectly; could be "+ aname + "_" + course)
        #     return False

        ar = [x[2] for x in os.walk(path)]
        print(ar)
        for folder in ar:
            if len(folder) == 0:
                print("Assignment is completely empty, needs a file.")
                return False
        # p1 = course.split("_")[0]
        # if(p1 in aname == False):
        #     print(aname + "incorrectly formated: must be " + aname + "_" + p1 + ".")
        #     return False
        try:
            datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
        except:
            print("Due-date format is incorrect")
            return False

        course = getDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/" + course)
        if aname in str(course['assignments']):
            print("Assignment name already taken.")
            return False
        print(course['assignments'])
        print(aname)
        #################### FINISH VERIFYING

        if not os.path.exists(os.getcwd() + "/" + self.username + "/Students/" + course['name']):
            print("No students in this class yet")
            return True
        slist = os.listdir(os.getcwd() + "/" + self.username + "/Students/" + course['name'])
        cdir = os.getcwd()
        for st in slist:
            if st in str(course['confirmed']):
                spath = os.path.join(os.getcwd() + "/" + self.username + "/Students/" + course['name'], st)
                if not os.path.exists(spath + "/" + aname):
                    os.mkdir(spath + "/" + aname)
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

        # check if assignment already exists
        r = requests.get(url='http://127.0.0.1:8000/api/assignments/' + aname, auth=(self.username, self.password))
        if r.status_code != 200:
            ass = {
                'name': oname,
                'path': path,
                'classes': course['name'],
                'teacher': self.username,
                'due_date': str(due),
                'owner':self.id
            }
            print(postDB(self.username, self.password, ass, 'http://127.0.0.1:8000/api/assignments/'))
            course['assignments'].append(oname)

            cinfo = {
                "assignments": course['assignments'],
            }
            print(patchDB(self.username, self.password, cinfo, "http://127.0.0.1:8000/api/classes/" + course['name'] + "/"))
            return True
        else:
            print("Assignment already addedd")
            return True

    # try to avoid
    # copy modified assignments to student directories
    def updateAssignment(self, path, course, due):
        parts = path.split("/")
        aname = parts[len(parts) - 1]
        oname = aname + "_" + course
        if not os.path.isdir(path):
            print(path + " is not an assignment.")
            return
        try:
            if due != None or due == "":
                datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
                d = {
                    'due_date': due,
                }
                print(patchDB(self.username, self.password, d, 'http://localhost:8000/api/assignments/' + oname + "/"))
                print("Due-date changed " + due)
        except:
            print("Due-date is the same")
        input()
        course = getDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/" + course)
        slist = os.listdir(os.getcwd() + "/" + self.username + "/Students/" + course['name'])
        cdir = os.getcwd()
        for st in slist:
            if st in course['confirmed']:
                spath = os.path.join(os.getcwd() + "/" + self.username + "/Students/" + course['name'], st)
                print(st)
                print(copy_tree(path, spath + "/" + aname))
                os.chdir(spath)
                # command('git checkout ' + course['name'])
                command('git add .')
                command('git commit -m Hello')
                command('git pull origin ' + course['name'])
                command('git push -u origin ' + course['name'])
                os.chdir(cdir)

    # pull student's work, no modifications
    def getStudents(self, course):
        if not (course in str(self.classes)):
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
        course = getDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/" + course)
        try:
            if not (student in course['confirmed']):
                print("Student not in class")
                return
        except:
            print("class does not exist")
            return

        cdir = os.getcwd()
        os.chdir(self.username + "/Students/" + course['name'] + "/" + student)
        process = subprocess.Popen(['git', 'log', '-' + str(commits), course['name']], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        p = process.poll()
        output = process.communicate()[0].decode('utf-8').split('\n\n')
        months = ['Jan', 'Feb', 'Mar', "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
        fout = []
        for i in range(len(output)):
            if "Date" in output[i]:
                c = output[i].split("\n")
                for k in range(len(c)):
                    temp = []
                    if 'commit' in c[k]:
                        c[k] = c[k].replace('commit', '').strip()
                    elif 'Date:' in c[k]:
                        c[k] = c[k].replace('Date:', '').strip()
                date = c[2].split(" ")
                times = date[3].split(":")
                mon = -1
                for m in range(len(months)):
                    if date[1] == months[m]:
                        mon = m
                d1 = datetime(int(date[4]), mon, int(date[2]), int(times[0]), int(times[1]))
                # datetime1 = datetime.strptime('07/11/2019 02:45PM', '%m/%d/%Y %I:%M%p')
                fout.append([c[0], d1])
                # output[i] = [c[0], d1]
                # print(output[i])
        print(fout)
        os.chdir(cdir)
        return fout

    def getChanges(self, student, course, commits):
        """
        Checks for new submissions by a student
        :param student: the student
        :param course: the course
        :param commits: commits the CLI has made for the assignment
        """
        course = getDB(self.username, self.password, "http://127.0.0.1:8000/api/classes/" + course + "/")
        ar = self.getCommits(student, course['name'], commits)
        commit = ar[len(ar) - 1][0]
        start = ""
        print("END:" + commit)
        print("START: " + start)
        cdir = os.getcwd()
        os.chdir(self.username + "/Students/" + course['name'] + "/" + student)
        process = subprocess.Popen(['git', 'diff', commit, '--name-status'], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        p = process.poll()
        output = process.communicate()[0].decode('utf-8')
        print(output)
        os.chdir(cdir)

        '''
        assignment = {
            'name': English11_eharris1,
            'due_date': 2020-06-11 16:58:33.383124
        }
        '''
        # check if assignment changed after due date

    def afterSubmit(self, course, assignment, student):

        assignment = getDB(self.username, self.password, "http://127.0.0.1:8000/api/assignments/" + assignment)
        # assignment = {
        #     'name': assignment,
        #     'due_date': "2020-04-11 16:58:33.383124",
        #     'classes':course
        # }
        log = self.getCommits(student, course, 30)
        assignment['due_date'] = datetime.strptime(assignment['due_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        late = False
        cdir = os.getcwd()
        os.chdir(self.username + "/Students/" + course + "/" + student)
        for l in log:
            process = subprocess.Popen(['git', 'show', l[0]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p = process.poll()
            output = process.communicate()[0].decode('utf-8')
            if assignment['name'] in output:
                print(l[1])
                print(assignment['due_date'])
                print("--------------")
                if l[1] > assignment['due_date']:
                    print("LATE")
                    os.chdir(cdir)
                    return True
        print("On time")
        os.chdir(cdir)
        return False

    def comment(self):
        """
        The ultimate form of laughter
        :return: pure joy
        """
        print("heheheh")


#data = getTeacher("eharris1",'hackgroup1')
# print(data)
#t = Teacher(data, 'hackgroup1')
#t.addAssignment("eharris1/Truck_eharris1/Assignment1", "Truck_eharris1", '2020-08-11 16:58:33.383124')

# t.makeClass("APLit_eharris1")
# t.updateAssignment("eharris1/APLit_eharris1/BookReport", "APLit_eharris1", '2020-08-11 16:58:33.383124')
# ar = ['2022rkhondak','2022inafi','2023rumareti']
# extra = t.reqAddStudentList(ar, "APLit_eharris1")
# print(extra)
# t.addStudent('2022rkhondak', 'APLit_eharris1')
# t.getChanges('2022rkhondak','APLit_eharris1', 10)

'''
{
    "name": "a",
    "due_date": '2020-08-11 16:58:33.383124',
    "path": "",
    "teacher": ""
}

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
