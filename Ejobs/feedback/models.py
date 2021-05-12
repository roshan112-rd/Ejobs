from django.db import models

# Create your models here.
class Feedback(models.Model):
    email = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)
    feedback = models.CharField(max_length=1050, null=True)

    def __str__(self):
        return self.email