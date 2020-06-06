from api.models import Assignment, Student, Classes, Teacher
from datetime import datetime    

#students
raffu = Student(
    first_name = "Raffu",
    last_name = "Khondaker",
    student_id = 1579460,
    webmail = "2022rkhondak@tjhsst.edu",
    grade = 10,
)
raffu.save()

#teachers
ng = Teacher(
    first_name = "Kim",
    last_name = "Ng",
)

ng.save()

chao = Teacher(
    first_name = "Susie",
    last_name = "Lebryk-Chao",
)

chao.save()

#Assignments
A1 = Assignment(
    name='Week1_HW',
    due_date=datetime.now(),
    
)
A1.save()

A2 = Assignment(
    name='Week2_HW',
    due_date=datetime.now(),
     
)
A2.save()

A3 = Assignment(
     name='Journal1',
     due_date=datetime.now(),
)
A3.save()

#classes
C1 = Classes(
    name='Math5',

)
C1.save()

C2 = Classes(
    name='English',
)
C2.save()

C2.teachers = chao
C2.students.add(raffu)
C2.save()

C1.teachers = ng
C1.students.add(raffu)
C1.save()

################################################################################################################
from api.models import Assignment, Student, Classes, Teacher
from datetime import datetime

A1 = Assignment(
    name='Week1_HW',
    due_date=datetime.now(),
    
)
A1.save()

A2 = Assignment(
    name='Week2_HW',
    due_date=datetime.now(),
     
)
A2.save()

A3 = Assignment(
     name='Journal1',
     due_date=datetime.now(),
)
A3.save()

#classes
math = Classes(
    name='Math5',

)
math.save()
math.assignments.add(A1)
math.assignments.add(A2)
math.save()

english = Classes(
    name='English',
)
english.save()
english.assignments.add(A3)
english.save()

#students
raffu = Student(
    first_name = "Raffu",
    last_name = "Khondaker",
    student_id = 1579460,
    webmail = "2022rkhondak@tjhsst.edu",
    grade = 10,
)
raffu.save()
raffu.classes.add(math)
raffu.classes.add(english)
raffu.save()

#teachers
ng = Teacher(
    first_name = "Kim",
    last_name = "Ng",
)
ng.save()
ng.classes.add(math)
ng.save()

chao = Teacher(
    first_name = "Susie",
    last_name = "Lebryk-Chao",
)
chao.save()
chao.classes.add(english)
chao.save()
