from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    job_id = models.AutoField(primary_key=True, null=False)
    JOB_CHOICES = (
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('webdesign', 'Webdesign'),
        ('management', 'Management'),
        ('technology', 'Technology'),
        ('hardware', 'hardware'),
        ('others', 'Others')
    )
    job_title = models.CharField(max_length=200)
    job_employer = models.CharField(max_length=100)
    job_position = models.CharField(max_length=200)
    job_category = models.CharField(max_length=250, choices=JOB_CHOICES, default='others')
    job_description = models.TextField()
    job_phone = models.CharField(max_length=100)
    job_email = models.EmailField()
    job_website = models.URLField()
    experience = models.TextField(null=False)    
    salary = models.CharField(max_length=100,null=True)
    job_location = models.CharField(max_length=100,null=True)
    no_of_vacancy = models.CharField(max_length=100,null=True)

    created = models.DateTimeField(auto_now_add=True)
    apply_until = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.job_title




class SavedJobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.job.job_title



class AppliedJobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    usercv = models.FileField(blank=True,null=True, upload_to='cv/')

    def __str__(self):
        return self.job.job_title
    