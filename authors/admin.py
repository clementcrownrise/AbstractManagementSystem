from django.contrib import admin
from . models import Authors
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fullname','email','phone')
    
admin.site.register(Authors,AuthorAdmin )

