from django.db import models

class DefFiles(models.Model):
    name=models.CharField(max_length=100)

class Assignment(models.Model):
    name=models.CharField(max_length=100)
    due_date=models.DateTimeField()
    files = models.ManyToManyField(DefFiles, default="")
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
    ion_user=models.CharField(primary_key=True, max_length=100)
    git = models.URLField(default="")

class Student(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.IntegerField()
    ion_user=models.CharField(primary_key=True, max_length=100)
    webmail = models.EmailField(blank=True)
    grade = models.IntegerField()
    git = models.URLField()
    classes = models.ManyToManyField(Classes, default="")
    repo = models.URLField(default="")

    def save(self, *args, **kwargs):
        return super(Student, self).save(*args, **kwargs)



