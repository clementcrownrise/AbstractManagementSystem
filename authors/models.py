from django.db import models
from article.models import Article, Casereport

# Create your models here.

class Authors(models.Model):
    article = models.ForeignKey('article.Article', on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='authors')
    casereport = models.ForeignKey('article.Casereport', on_delete=models.SET_NULL, blank=True, 
                                   null=True, related_name='authors')
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    affiliation = models.CharField(max_length=200)



    def __str__(self):
        return self.fullname
    

