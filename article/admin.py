from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('conference','title','user','status','submitted_at')

admin.site.register(Article, ArticleAdmin)




