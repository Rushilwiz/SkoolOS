from django.contrib.auth.models import Group

g, created = Group.objects.get_or_create(name='teachers')

# from datetime import datetime
#
# f1 = DefFiles(
#     name="instructions.txt"
# )
# f1.save()
# f2 = DefFiles(
#     name="instructions.txt"
# )
# f2.save()
# f3 = DefFiles(
#     name="sample.txt"
# )
# f3.save()
# f4 = DefFiles(
#     name="rubric.txt"
# )
# f4.save()
#
# a1 = Assignment.objects.get(pk=1)
# a1.files.add(f1)
# a1.save()
# a2 = Assignment.objects.get(pk=2)
# a2.files.add(f2)
# a2.save()
# a3 = Assignment.objects.get(pk=3)
# a3.files.add(f3)
# a3.files.add(f4)
# a3.save()
#
# ####################################
#
# from api.models import Assignment, Student, Class, Teacher, DefFiles
# from datetime import datetime
#
# f1 = DefFiles(
#     name="instructions.txt"
# )
# f1.save()
# f2 = DefFiles(
#     name="instructions.txt"
# )
# f2.save()
# f3 = DefFiles(
#     name="sample.txt"
# )
# f3.save()
# f4 = DefFiles(
#     name="rubric.txt"
# )
# f4.save()
#
# A1 = Assignment(
#     name='Week1_HW',
#     due_date=datetime.now(),
# )
# A1.save()
# A1.files.add(f1)
# A1.save()
#
# A2 = Assignment(
#     name='Week2_HW',
#     due_date=datetime.now(),
#
# )
# A2.save()
# A2.files.add(f2)
# A2.save()
#
# A3 = Assignment(
#      name='Journal1',
#      due_date=datetime.now(),
# )
# A3.save()
# A3.files.add(f3)
# A3.files.add(f4)
# A3.save()
#
# #Class
# math = Class(
#     name='Math5',
#
# )
# math.save()
# math.assignments.add(A1)
# math.assignments.add(A2)
# math.save()
#
# english = Class(
#     name='English',
# )
# english.save()
# english.assignments.add(A3)
# english.save()
#
# #students
# raffu = Student(
#     first_name = "Raffu",
#     last_name = "Khondaker",
#     student_id = 1579460,
#     ion_user="2022rkhondak",
#     webmail = "2022rkhondak@tjhsst.edu",
#     grade = 10,
#     repo="https://github.com/therealraffi/2022rkhondak.git",
# )
# raffu.save()
# raffu.Class.add(math)
# raffu.Class.add(english)
# raffu.save()
#
# #teachers
# ng = Teacher(
#     first_name = "Errin",
#     last_name = "Harris",
#     ion_user="eharris1"
# )
# ng.save()
# ng.Class.add(math)
# ng.save()
#
# chao = Teacher(
#     first_name = "Abagail",
#     last_name = "Bailey",
#     ion_user="AKBailey"
# )
# chao.save()
# chao.Class.add(english)
# chao.save()
