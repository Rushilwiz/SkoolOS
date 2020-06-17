Command Line Interface
=====================

Making a user:
-------
::
    python skoolos.py

You will be redirected to a login page for the SkoolOS website. If you have already created an account on the website, enter login informatiton. If not, select
the registration button bellow and create an account. Once you create an account via Ion OAuth and SkoolOS, login. The window should close, prompting:

Enter SkoolOS Username:
Enter SkoolOS Password:

Enter the valid SkoolOS username and password. Congratialations, you have successfully logged in.

1. CLI as a teacher:
============

Start the CLI and select your username. For instance, teacher 'eharris1'::
    
    python skoolos.py
    ? Select User:   (Use arrow keys)
    1) 2022rkhondak
    ❯ 2) eharris1
    3) Make new user

You will then be given the choice to select an existing class, Make a new class, or exit the CLI:
::

    ? Select class:   (Use arrow keys)
     ❯ Art12_eharris1
       English12_eharris1
       History12_eharris1
       Make New Class
       Exit SkoolOS

Making a new class:
-------

Select 'Make a New Class'. You will then be prompted to enter a class name. The format for every  class must be <subject>_<teacher_username> (Example: Art12_eharris1). 
Enter Period (must be a positive integer). You will then be prompted to add students. If you have a list of students, enter the relative path of a text file with the student usernames.
The file must be a .txt file and have one student username per line. If you add an individual student, simply enter their ion username.
one username per line.::

    ? Select class:   (Use arrow keys)
       Art12_eharris1
       English12_eharris1
       History12_eharris1
     ❯ Make New Class
       Exit SkoolOS
    
    ? Add Students):   (Use arrow keys)
     ❯ 1) Add individual student
       2) Add list of students through path
       3) Exit
    
    ? Add Students):   2) Add list of students through path
    File must be .txt and have 1 student username per line
    Relative Path: students.txt

OR::

    ? Add Students):   1) Add individual student
    Student name: 2022rkhondak

Accessing an existing class
=====================

Once you have created a class, you can then view and modify certain fields. (Open opening a class, any students who have accepted the request will be automatically
added you the class.)::

    ? Select class:   (Use arrow keys)
       Art12_eharris1
       Civ_eharris1
     ❯ English12_eharris1
       History12_eharris1
       Random_eharris1
       Truck_eharris1
       Make New Class
       Exit SkoolOS
    
    Class: English12_eharris1
    ? Select option:   (Use arrow keys)
     ❯ 1) Request Student
       2) Add assignment
       3) View student information
       4) Exit

Requesting Students
-------

Select 'Request Student'. You will then be prompted to add students. If you have a list of students, enter the relative path of a text file with the student usernames.
The file must be a .txt file and have one student username per line. If you add an individual student, simply enter their ion username.
one username per line.::

    Class: English12_eharris1
    ? Select option:   (Use arrow keys)
     ❯ 1) Request Student
       2) Add assignment
       3) View student information
       4) Exit
    
    ? Add list of students (input path):   (Use arrow keys)
     ❯ 1) Add individual student
       2) Add list of students through path
       3) Exit
    
    ? Select option:   1) Request Student
    ? Add list of students (input path):   1) Add individual student
    ? Student Name:   2022rkhondak

OR::

    ? Add Students):   2) Add list of students through path
    File must be .txt and have 1 student username per line
    Relative Path: students.txt

Adding an assignment
-------

To add an assignment, make an assginment subdirectory in the corresponding class wiht at least 1 file. Somehting like:

  eharris1/English12_eharris1/Assignment1/instruct.txt

You must also put a due date in the correct format.::

  ? Select new assignment:   Assignment1
  Enter due date (Example: 2020-08-11 16:58):  2020-08-11 16:58

View student information
-------

You can view certain information of any student requested or confirmed in the given class. Simply select enter their name and see their profile. You are also given the choice
to view their logs (files they have saved, written, git commands, and file that dont match the extention whitelist). Note that as a teacher, you can view a student's current
work at ANY TIME. Simply go to the 'Students' directory and select the student's directory.::

  eharris1/Students/English12_eharris1/2022rkhondak
  eharris1/Students/English12_eharris1/2023rumareti

  ? Select option:   (Use arrow keys)
   1) Request Student
   2) Add assignment
    ❯ 3) View student information
   4) Exit

   Students in class: 
   2022rkhondak
   Requsted Students: 
   2023rumareti
   View student (Enter student's ion username):


2. CLI as a student:
============

As a student, you can edit your work for certain classes and submit assignments. By default, your workr directory (your username) has a single readme. AND IT SHOULD STAY THAT WAY.
To make changes to a class, you must first select that class via the CLI.::

  Select a class first:
    ? Select class:   (Use arrow keys)
    English12_eharris1
    Art12_eharris1
    ❯ Random_eharris1
    Exit SkoolOS

You can then view the assignments associated with the class. Open you work directory and modify files within your assignments. At any time, you can 'Save' or go 'Back'. 
When you are ready, you can submit an assignment:
::

  ? Select:   (Use arrow keys)
    Save
   ❯  Submit assignment
    Back
    Exit SkoolOS

    ? Select:   (Use arrow keys)
    Assignment1
    ❯ Back
