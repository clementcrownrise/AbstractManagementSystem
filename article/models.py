from django.db import models
from accounts.models import Account
from conference.models import Conference
from faculty.models import Faculty
from reviewers.models import Reviewer
#from ckeditor.fields import RichTextField
#from django_summernote.fields import SummernoteTextField
from tinymce.models import HTMLField
import uuid

# Create your models here.

class Casereport(models.Model):
    ARTICLE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    )
    
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    abstracttype = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, unique=True)
    presentername = models.CharField(max_length=200)
    presenteremail = models.CharField(max_length=200)
    presenterphone = models.CharField(max_length=200)
    casereport =  HTMLField()
    keywords = models.CharField(max_length=200)
    frtitle = models.CharField(max_length=300)
    frcasereport =  HTMLField()
    frkeywords = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=ARTICLE_STATUS_CHOICES, default='pending')
    submitted_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Article(models.Model):
    ARTICLE_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    )

    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    abstracttype = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, unique=True)
    presentername = models.CharField(max_length=200)
    presenteremail = models.CharField(max_length=200)
    presenterphone = models.CharField(max_length=200)
    introduction =  HTMLField()
    methods =  HTMLField()
    results =  HTMLField()
    conclusion =  HTMLField()
    limitations =  HTMLField()
    keywords = models.CharField(max_length=200)
    frtitle = models.CharField(max_length=300)
    frintroduction =  HTMLField()
    frmethods =  HTMLField()
    frresults =  HTMLField()
    frconclusion =  HTMLField()
    frlimitations =  HTMLField()
    frkeywords = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=ARTICLE_STATUS_CHOICES, default='pending')
    submitted_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title




class ArticleReviewer(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True )
    casereport = models.ForeignKey(Casereport, on_delete=models.CASCADE, null=True, blank=True )
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    reviewed = models.BooleanField(default=False)
    assigned_at = models.DateField(auto_now_add=True)
    submitted_at = models.DateField(auto_now_add=True)

    


class Comment(models.Model):
    COMMENT_STATUS_CHOICES =(
        ('approved', 'Approved'),
        ('minor revision', 'Minor Revisions'),
        ('major revision', 'Major Revisions'),
        ('rejected','Rejected'),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, 
                                related_name='comments', null=True, blank=True)
    casereport = models.ForeignKey(Casereport, on_delete=models.CASCADE, 
                                   related_name='comments', null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment = HTMLField()
    status = models.CharField(max_length=20, choices=COMMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class ReviewerReport(models.Model):
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE,related_name='reviewer_reports' )
    casereport = models.ForeignKey(Casereport, blank=True, null=True, on_delete=models.CASCADE, related_name='reviewer_reports')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)
    titlescore = models.DecimalField( max_digits=3,
    decimal_places=1)
    introductionscore = models.DecimalField( max_digits=3,
    decimal_places=1)
    methodscore = models.DecimalField( max_digits=3,
    decimal_places=1)
    resultscore = models.DecimalField( max_digits=3,
    decimal_places=1)
    conclusionscore = models.DecimalField( max_digits=3,
    decimal_places=1)
    overallscore = models.DecimalField( max_digits=3,
    decimal_places=1)
    totalscore = models.DecimalField( max_digits=3,
    decimal_places=1)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

