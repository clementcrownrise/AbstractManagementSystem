from django import forms
from .models import Article
from accounts.models import Account
from conference.models import Conference
from django.utils import timezone
#from ckeditor.widgets import CKEditorWidget
#from ckeditor.fields import RichTextField
#from django_summernote.widgets import SummernoteWidget
from tinymce.widgets import TinyMCE


class ArticleForm(forms.ModelForm):
    introduction = forms.CharField(widget=TinyMCE())

    
    class Meta:
        model = Article
        fields = [
            'conference',
            'title',
            'introduction',
            'paymentevidence',
            'document',
        ]

        widgets = {
            'conference': forms.Select(attrs={'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'paymentevidence': forms.FileInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'introduction':forms.CharField(widget=TinyMCE()),

        }

    def clean_document(self):
        document = self.cleaned_data.get('document')
        if document:
            allowed_extensions = ['.doc', '.docx']

            if not any(document.name.lower().endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError(
                    "Only DOC or DOCX files are allowed for Abstracts."
                )

        return document
    
    def clean_paymentevidence(self):
        paymentevidence = self.cleaned_data.get('paymentevidence')
        if paymentevidence:
            allowed_extensions = ['.jpg','.jpeg','.png']

            if not any(paymentevidence.name.lower().endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError(
                    "Only .jpeg, .png and .jpg files are allowed for payment evidence"
                )
        return paymentevidence
      


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now().date()
        self.fields['conference'].queryset = Conference.objects.filter(
             closing_date__gt=today
    )