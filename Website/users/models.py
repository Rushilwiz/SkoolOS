from django.db import models
from uuid import uuid4


# Create your models here.

class Token(models.Model):
    username = models.TextField()
    email = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    grade = models.IntegerField(default=9)
    isStudent = models.BooleanField(default=True)
    token = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid4()
        return super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}'s Token";
