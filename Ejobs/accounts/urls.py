from django.urls import path
from . import views

urlpatterns = [
    path('seeker_register/', views.seeker_register, name='seeker_register'),
    # path('seeker_login/', views.seeker_login, name='seeker_login'),
    path('seeker_dashboard/', views.seeker_dashboard, name='seeker_dashboard'),
    path('seeker_profile/', views.seeker_profile, name='seeker_profile'),

    path('recruiter_register/', views.recruiter_register, name='recruiter_register'),
    # path('recruiter_login/', views.recruiter_login, name='recruiter_login'),
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter_profile/', views.recruiter_profile, name='recruiter_profile'),
    
    path('additional_details/', views.additional_details, name='additional_details'),
    path('social_details/', views.social_details, name='social_details'),
    path('logout', views.logout, name='logout'),
    path('login/', views.login, name='login'),  
]