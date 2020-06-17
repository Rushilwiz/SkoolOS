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

Start the CLI and select your username. For instance, teacher 'eharris1'

python skoolos.py
.. code-block:: python
    ? Select User:   (Use arrow keys)
    1) 2022rkhondak
    ❯ 2) eharris1
    3) Make new user

You will then be given the choice to select an existing class, Make a new class, or exit the CLI:

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
one username per line.

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

OR 

? Add Students):   1) Add individual student
Student name: 2022rkhondak

Accessing an existing class
=====================

Once you have created a class, you can then view and modify certain fields. (Open opening a class, any students who have accepted the request will be automatically
added you the class.)

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








