from django.db import models

class Student(models.Model):
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.IntegerField(primary_key=True)
    webmail = models.EmailField(blank=True)
    grade = models.IntegerField()
    classes = models.ForeignKey('Classes', on_delete=models.CASCADE,blank=True)

class Teacher(models.Model):
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    #student_id = models.IntegerField(primary_key=True)    

class Classes(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=100)
    teachers = models.ForeignKey('Teacher', on_delete=models.CASCADE,null=True)

    def save(self, *args, **kwargs):
        return super(Classes, self).save(*args, **kwargs)

class Assignment(models.Model):
    url = models.URLField()
    name=models.CharField(max_length=100)
    due_date=models.DateTimeField()

    def __str__(self):
        return '%d' % (self.name)


