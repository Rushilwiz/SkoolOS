import subprocess
import os

#students
def initialize(repo, subject):
    process = subprocess.Popen(['git', 'clone', repo], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = process.communicate()
    dirname = repo[repo.rindex('/')+1:repo.index(".git")]
    os.rename(dirname, subject)
    #print(output)

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


initialize("https://github.com/therealraffi/1579460.git", "Math1")
