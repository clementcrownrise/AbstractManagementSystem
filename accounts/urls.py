from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    #path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register-reviewer/', views.registerreviewer, name='register-reviewer'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    

    path('resetPassword_validate/<uidb64>/<token>/', views.resetPassword_validate, name='resetPassword_validate'),
    path('forgot-password/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

]