from django.contrib import admin
from .models import Reviewer
# Register your models here.

class ReviewerAdmin(admin.ModelAdmin):
    list_display=('fullname','email','faculty',)


admin.site.register(Reviewer, ReviewerAdmin)
