from django.db import models

class DefFiles(models.Model):
    name=models.CharField(max_length=100)
    path=models.CharField(max_length=100)
    assignment=models.CharField(max_length=100, default="")
    classes=models.CharField(max_length=100)
    teacher=models.CharField(max_length=100)

class Assignment(models.Model):
    name=models.CharField(max_length=100)
    due_date=models.DateTimeField()
    # files = models.ManyToManyField(DefFiles)
    files=models.CharField(max_length=100)
    path=models.CharField(max_length=100)
    classes=models.CharField(max_length=100)
    teacher=models.CharField(max_length=100)
    def __str__(self):
        return '%s' % (self.name)

class Classes(models.Model):
    name = models.CharField(max_length=100)
    repo=models.URLField(default="")
    path=models.CharField(max_length=100, default="")
    teacher=models.CharField(max_length=100, default="")
    assignments=models.CharField(max_length=100, default="")
    default_file=models.CharField(max_length=100, default="")
    confirmed=models.TextField(default="", blank=True)
    unconfirmed=models.TextField(default="", blank=True)

    # assignments = models.ManyToManyField(Assignment, default="")
    # default_file = models.ManyToManyField(DefFiles)
    def save(self, *args, **kwargs):
        return super(Classes, self).save(*args, **kwargs)

class Teacher(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # classes = models.ManyToManyField(Classes, default="")
    classes=models.CharField(max_length=100, default="", blank=True)
    ion_user=models.CharField(primary_key=True, max_length=100)
    git=models.CharField(max_length=100)
    email=models.CharField(max_length=100, default="", blank=True)

class Student(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.IntegerField()
    ion_user=models.CharField(primary_key=True, max_length=100)
    email=models.CharField(max_length=100, default="", blank=True)
    grade = models.IntegerField()
    git=models.CharField(max_length=100)
    repo=models.URLField(default="", blank=True)
    classes=models.CharField(max_length=100, default="", blank=True)
    added_to=models.CharField(max_length=100, default="", blank=True)
    completed=models.TextField(default="", blank=True)
    
    def save(self, *args, **kwargs):
        return super(Student, self).save(*args, **kwargs)



