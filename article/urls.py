from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.create_abstract, name='create_abstract'),
    path('casereport/', views.create_casereport, name='create_casereport'),
    path('detailedpage/<int:id>/', views.view_abstract, name='detailedpage'),
    path('detailedpage/casereport/<int:id>/', views.view_casereport, name='casedetailedpage'),
    path('assign_reviewer/<int:pk>/', views.assign_reviewer, name='assign_reviewer'),
    path('assign_reviewer_casereport/<int:pk>/', views.casereportassign_reviewer, 
         name='casereportassign_reviewer'),
    path('comment/<int:pk>/', views.admin_comment, name='comment'),
    path('comment/casereport/<int:pk>/', views.admin_casereportcomment, name='casereportcomment'),
    path('faculylisting/<int:pk>/', views.facultylisting, name='faculylisting'),
    path('remove_reviewer/<int:article_id>/<int:reviewer_id>/', views.remove_reviewer, name ='remove_reviewer'),
    path('remove_reviewercasereport/<int:casereport_id>/<int:reviewer_id>/', 
         views.remove_reviewercasereport, name ='remove_reviewercasereport'),

    path('review/<uuid:token>/', views.review_article, name='review_article'),
    path('reviewcasereport/<uuid:token>/', views.review_casereport, name='review_casereport'),

    path('reviewerResult/<int:pk>/', views.reviewerResult, name='reviewerResult'),

    path('export', views.exportall, name='export')



]