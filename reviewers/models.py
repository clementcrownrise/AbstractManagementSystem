from django.db import models
from faculty.models import Faculty

# Create your models here.

class Reviewer(models.Model):
    faculty = models.ForeignKey('faculty.Faculty',on_delete=models.SET_NULL, null=True, blank=True)
    fullname = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100, default='reviewer')


    def __str__(self):
        return self.fullname