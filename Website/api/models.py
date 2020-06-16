from django.db import models
from django.contrib.auth.models import User
import secrets



class Student(models.Model):
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE)
    ion_user = models.CharField(max_length=100, primary_key=True)
    grade = models.IntegerField(default=0, blank=True)
    git=models.CharField(default="", max_length=100, blank=True)
    repo=models.URLField(default="", blank=True)
    classes=models.CharField(max_length=100, default="", blank=True)
    added_to=models.CharField(max_length=100, default="", blank=True)
    completed=models.TextField(default="", blank=True)

    def save(self, *args, **kwargs):
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Assignment(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, related_name='aowner', on_delete=models.CASCADE)

    name=models.CharField(max_length=100, primary_key=True)
    due_date=models.DateTimeField()
    # files = models.ManyToManyField(DefFiles)
    files=models.CharField(max_length=100, default="", blank=True)
    path=models.CharField(max_length=100)
    classes=models.CharField(max_length=100)
    teacher=models.CharField(max_length=100)
    def __str__(self):
        return '%s' % (self.name)


class Class(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, related_name='cowner', on_delete=models.CASCADE)
    teacher = models.CharField(max_length=100)
    name = models.CharField(primary_key=True, max_length=100)
    id = models.CharField(max_length=8, blank=True, null=True)
    description = models.CharField(default="Class Description", max_length=500)
    repo=models.URLField(default="", blank=True)
    path=models.CharField(max_length=100, default="")
    assignments=models.ManyToManyField(Assignment, blank=True)
    default_file=models.CharField(max_length=100, default="", blank=True)
    confirmed=models.ManyToManyField(Student, blank=True, related_name='confirmed')
    unconfirmed=models.ManyToManyField(Student, blank=True, related_name='unconfirmed')

    # assignments = models.ManyToManyField(Assignment, default="")
    # default_file = models.ManyToManyField(DefFiles)
    def save(self, *args, **kwargs):
        id = self.id
        if not id:
            id = secrets.token_urlsafe()[:8].lower()
        while Class.objects.filter(id=id).exclude(pk=self.pk).exists():
            id = secrets.token_urlsafe()[:8].lower()
        self.id = id
        return super(Class, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classes=models.ManyToManyField(Class, blank=True, related_name='classes')
    git=models.CharField(max_length=100, default="", blank=True)
    ion_user=models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        super(Teacher, self).save(*args, **kwargs)

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     ion_user=models.CharField(primary_key=True, max_length=100)
#     grade = models.IntegerField(default=0, blank=True)
#     git=models.CharField(default="", max_length=100, blank=True)
#     repo=models.URLField(default="", blank=True)
#     classes=models.CharField(max_length=100, default="", blank=True)
#     added_to=models.CharField(max_length=100, default="", blank=True)
#     completed=models.TextField(default="", blank=True)


class DefFiles(models.Model):
    name=models.CharField(max_length=100)
    path=models.CharField(max_length=100)
    assignment=models.CharField(max_length=100, default="")
    classes=models.CharField(max_length=100)
    teacher=models.CharField(max_length=100)
