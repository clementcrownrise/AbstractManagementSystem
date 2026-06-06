from django import forms
from .models import Article, Casereport
from accounts.models import Account
from conference.models import Conference
from django.utils import timezone
#from ckeditor.widgets import CKEditorWidget
#from ckeditor.fields import RichTextField
#from django_summernote.widgets import SummernoteWidget
from tinymce.widgets import TinyMCE
from django.forms import inlineformset_factory
from authors.models import Authors
from django.core.exceptions import ValidationError

class CasereportForm(forms.ModelForm):
    abstracttype = forms.Select(attrs={'class':'form-control'})
    conference = forms.Select(attrs={'class':'form-control'})
    faculty = forms.Select(attrs={'class':'form-control'})
    title = forms.TextInput(attrs={'class':'form-control'})
    presentername = forms.TextInput(attrs={'class':'form-control'})
    presenteremail = forms.TextInput(attrs={'class':'form-control'})
    presenterphone = forms.TextInput(attrs={'class':'form-control'})
    casereport = forms.CharField(widget=TinyMCE())
    keywords = forms.TextInput(attrs={'class':'form-control'})
    #frenchversion below
    frtitle = forms.TextInput(attrs={'class':'form-control'})
    frcasereport = forms.CharField(widget=TinyMCE())
    frkeywords = forms.TextInput(attrs={'class':'form-control'})
    
    class Meta:
        model = Casereport
        exclude = ['user','status']

        widgets = {
            'abstracttype' : forms.Select(attrs={'class':'form-control'}),
            'conference': forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'faculty': forms.Select(attrs={'class':'form-control'}),
            'presentername': forms.TextInput(attrs={'class':'form-control'}),
            'presenteremail': forms.TextInput(attrs={'class':'form-control'}),
            'presenterphone': forms.TextInput(attrs={'class':'form-control'}),
            'casereport':forms.CharField(widget=TinyMCE()),
            'keywords': forms.TextInput(attrs={'class':'form-control'}),
            #frenchversion below
            'frtitle': forms.TextInput(attrs={'class':'form-control'}),
            'frcasereport':forms.CharField(widget=TinyMCE()),
            'frkeywords': forms.TextInput(attrs={'class':'form-control'}),


        }

class ArticleForm(forms.ModelForm):
    abstracttype = forms.Select(attrs={'class':'form-control'})
    conference = forms.Select(attrs={'class':'form-control'})
    faculty = forms.Select(attrs={'class':'form-control'})
    title = forms.TextInput(attrs={'class':'form-control'})
    presentername = forms.TextInput(attrs={'class':'form-control'})
    presenteremail = forms.TextInput(attrs={'class':'form-control'})
    presenterphone = forms.TextInput(attrs={'class':'form-control'})
    introduction = forms.Textarea(attrs={'class':'form-control wordbox','rows':6})
    methods = forms.Textarea()
    results = forms.Textarea()
    conclusion = forms.Textarea()
    limitations=forms.Textarea()
    keywords = forms.TextInput(attrs={'class':'form-control'})
    #frenchversion below
    frtitle = forms.TextInput(attrs={'class':'form-control'})
    frintroduction = forms.CharField(widget=TinyMCE())
    frmethods = forms.CharField(widget=TinyMCE())
    frresults = forms.CharField(widget=TinyMCE())
    frconclusion = forms.CharField(widget=TinyMCE())
    frlimitations=forms.CharField(widget=TinyMCE())
    frkeywords = forms.TextInput(attrs={'class':'form-control'})
    #let;s seehere


    class Meta:
        model = Article
        exclude = ['user','status']
        

        widgets = {
            'abstracttype' : forms.Select(attrs={'class':'form-control'}),
            'conference': forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'faculty': forms.Select(attrs={'class':'form-control'}),
            'presentername': forms.TextInput(attrs={'class':'form-control'}),
            'presenteremail': forms.TextInput(attrs={'class':'form-control'}),
            'presenterphone': forms.TextInput(attrs={'class':'form-control'}),
            'introduction':forms.Textarea(attrs={'class':'form-control wordbox','rows':6}),
            'methods':forms.Textarea(attrs={'class':'form-control wordbox','rows':6}),
            'results':forms.Textarea(attrs={'class':'form-control wordbox','rows':6}),
            'conclusion':forms.Textarea(attrs={'class':'form-control wordbox','rows':6}),
            'limitations':forms.Textarea(attrs={'class':'form-control wordbox','rows':6}),
            'keywords': forms.TextInput(attrs={'class':'form-control'}),
            #frenchversion below
            'frtitle': forms.TextInput(attrs={'class':'form-control'}),
            'frintroduction':forms.CharField(widget=TinyMCE()),
            'frmethods':forms.CharField(widget=TinyMCE()),
            'frresults':forms.CharField(widget=TinyMCE()),
            'frconclusion':forms.CharField(widget=TinyMCE()),
            'frlimitations':forms.CharField(widget=TinyMCE()),
            'frkeywords': forms.TextInput(attrs={'class':'form-control'}),


        }

      
      


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.fields['conference'].queryset = Conference.objects.filter(
             closing_date__gt=today
    )
    
    def clean(self):

        cleaned_data = super().clean()

        fields = [
            'introduction',
            'methods',
            'results',
            'conclusion',
            'limitations'
        ]

        total_words = 0

        for field in fields:
            text = cleaned_data.get(field, '')
            total_words += len(text.split())

        if total_words > 400:
            raise ValidationError(
                f'Total word count is {total_words}. Maximum allowed is 400.'
            )

        return cleaned_data