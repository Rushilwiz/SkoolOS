from django.db import models

class Assignment(models.Model):
    name=models.CharField(max_length=100)
    due_date=models.DateTimeField()
    def __str__(self):
        return '%s' % (self.name)

class Classes(models.Model):
    name = models.CharField(max_length=100)
    assignments = models.ManyToManyField(Assignment, default="")
    def save(self, *args, **kwargs):
        return super(Classes, self).save(*args, **kwargs)

class Teacher(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Classes, default="")

class Student(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.IntegerField(primary_key=True)
    webmail = models.EmailField(blank=True)
    grade = models.IntegerField()
    classes = models.ManyToManyField(Classes, default="")
    def save(self, *args, **kwargs):
        return super(Student, self).save(*args, **kwargs)



