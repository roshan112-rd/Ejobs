from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.




admin.site.site_header = 'Admin dashboard'

class SeekerAdmin(admin.ModelAdmin):
    list_display = ('user','address','contact')
    list_filter = ('created',)





admin.site.register(Seeker,SeekerAdmin)
admin.site.register(Recruiter)
admin.site.register(SeekerAdditionalDetails)
admin.site.register(SeekerSocialDetails)
admin.site.unregister(Group)
admin.site.register(Token)