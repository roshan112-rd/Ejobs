from django.urls import path
from . import views


urlpatterns = [
    path('password_change/', views.password_change, name='password_change'), 
    path('edit_add_details/', views.edit_add_details, name='edit_add_details'),
    path('edit_social_data/', views.edit_social_data, name='edit_social_data'),
    path('edit_user_data/', views.edit_user_data, name='edit_user_data'),
    path('edit_recruiter_data/', views.edit_recruiter_data, name='edit_recruiter_data'),
    path('pp_change/', views.pp_change, name='pp_change'),
    path('change_pp/', views.change_pp, name='change_pp'),
    path('remove_social/', views.remove_social, name='remove_social'),
    path('remove_add/', views.remove_add, name='remove_add'),
]