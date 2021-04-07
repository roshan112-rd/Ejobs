from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.feedback, name='feedback'), 
    path('about_us/', views.about_us, name='about_us'),
]