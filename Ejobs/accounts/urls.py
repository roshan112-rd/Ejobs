from django.urls import path
from . import views


urlpatterns = [
    path('seeker_register/', views.seeker_register, name='seeker_register'),
    path('seeker_dashboard/', views.seeker_dashboard, name='seeker_dashboard'),
    path('recruiter_register/', views.recruiter_register, name='recruiter_register'),
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('additional_details/', views.additional_details, name='additional_details'),
    path('social_details/', views.social_details, name='social_details'),
    
    path('logout', views.logout, name='logout'),
    path('login/', views.login, name='login'), 
    path('profile/', views.profile, name='profile'),
    
    path('success/<auth_token>', views.success, name='success'),

]