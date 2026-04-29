from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.create_abstract, name='create_abstract'),
    path('detailedpage/<int:id>/', views.view_abstract, name='detailedpage'),
    path('assign_reviewer/<int:pk>/', views.assign_reviewer, name='assign_reviewer'),
    path('comment/<int:pk>/', views.admin_comment, name='comment'),
    path('remove_reviewer/<int:article_id>/<int:reviewer_id>/', views.remove_reviewer, name ='remove_reviewer'),
]