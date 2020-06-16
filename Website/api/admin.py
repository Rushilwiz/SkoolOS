from django.contrib import admin
from .models import (
    DefFiles,
    Assignment,
    Class,
    Teacher,
    Student
)

# Register your models here.

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(DefFiles)
admin.site.register(Assignment)
admin.site.register(Class)
