from django.contrib import admin
from .models import Faculty

# Register your models here.

class FacultyAdmin(admin.ModelAdmin):
        list_display = ('faculty_name',)

    

admin.site.register(Faculty, FacultyAdmin)
