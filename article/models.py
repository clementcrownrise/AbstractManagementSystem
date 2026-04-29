from django.db import models
from accounts.models import Account
from conference.models import Conference
#from ckeditor.fields import RichTextField
#from django_summernote.fields import SummernoteTextField
from tinymce.models import HTMLField

# Create your models here.
class Article(models.Model):
    ARTICLE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    #introduction = SummernoteTextField()
    introduction =  HTMLField()
    paymentevidence= models.FileField(upload_to='paymentevidence/')
    document = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=ARTICLE_STATUS_CHOICES, default='pending')
    submitted_at = models.DateField(auto_now_add=True)


class ArticleReviewer(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE )
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE)
    assigned_at = models.DateField(auto_now_add=True)
    submitted_at = models.DateField(auto_now_add=True)


class Comment(models.Model):
    COMMENT_STATUS_CHOICES =(
        ('approved', 'Approved'),
        ('minor revision', 'Minor Revisions'),
        ('major revision', 'Major Revisions'),
        ('rejected','Rejected'),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment = HTMLField()
    status = models.CharField(max_length=20, choices=COMMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)