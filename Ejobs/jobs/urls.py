from django.urls import path
from. import views


urlpatterns = [
    path('add_job/', views.add_job, name='add_job'),
    path('jobhome/', views.jobhome, name='jobhome'),

    path('jobs/', views.jobs, name='jobs'),
    path('delete_job/<int:id>', views.delete_job, name='delete_job'),
    path('saved_jobs/', views.saved_jobs, name='saved_jobs'),
    path('appliedJobs/', views.appliedJobs, name='appliedJobs'),
    path('save_job/<int:job_id>', views.save_job, name='save_job'),
    path('apply_job/<int:job_id>', views.apply_job, name='apply_job'),
    path('remove_job/<int:id>', views.remove_job, name='remove_job'),
    path('applicants/', views.applicants, name='applicants'),
    path('applicants/<int:job_id>', views.applicant, name='applicant'),
    path('job_details/<int:id>', views.job_details, name='job_details'),
    path('remove_applied_job/<int:id>', views.remove_applied_job, name='remove_applied_job'),

    path("search/", views.search, name="search"),
    path("accept/<int:id>/", views.accept, name="accept"),
    path("decline/<int:id>/", views.decline, name="decline"),
    path('job_details_2/<int:id>', views.job_details_2, name='job_details_2'),
    path('edit_job/<int:job_id>', views.edit_job, name='edit_job'),
]