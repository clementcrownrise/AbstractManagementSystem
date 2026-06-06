from django.contrib import admin
from .models import Article, Casereport, ArticleReviewer, Comment, ReviewerReport

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    
    
    list_display = ('conference','title','user','status','submitted_at')

admin.site.register(Article, ArticleAdmin)




class CasereportAdmin(admin.ModelAdmin):
    list_display = ('conference','abstracttype', 'title','user', 'status', 'submitted_at')
admin.site.register(Casereport, CasereportAdmin)


class ArticleReviewerAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.article_id
    
    list_display=('article','casereport','reviewed','token','reviewer')
admin.site.register(ArticleReviewer, ArticleReviewerAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display=('article','comment','article','user','casereport')
admin.site.register(Comment, CommentAdmin )


class ReviewerReportAdmin(admin.ModelAdmin):
    list_display = ('article','casereport','reviewer',
                    'introductionscore',
                    'methodscore',
                    'resultscore',
                    'conclusionscore',
                    'overallscore',
                    'comments',
                    'created_at')
admin.site.register(ReviewerReport, ReviewerReportAdmin)