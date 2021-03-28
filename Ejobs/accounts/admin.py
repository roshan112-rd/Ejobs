from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Seeker)
admin.site.register(Recruiter)
admin.site.register(SeekerAdditionalDetails)
admin.site.register(SeekerSocialDetails)

