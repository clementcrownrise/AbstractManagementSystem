from django.db import models

# Create your models here.
class Conference(models.Model):
    name = models.CharField(max_length=100, unique=True)
    closing_date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)



    def __str__(self):
        return self.name