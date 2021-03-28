from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import *

class SeekerSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    location = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_seeker = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        seeker = Seeker.objects.create(user=user)
        seeker.phone_number=self.cleaned_data.get('phone_number')
        seeker.location=self.cleaned_data.get('location')
        seeker.save()
        return user

class RecruiterSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    designation = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_recruiter = True
        user.is_staff = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        recruiter = Recruiter.objects.create(user=user)
        recruiter.phone_number=self.cleaned_data.get('phone_number')
        recruiter.designation=self.cleaned_data.get('designation')
        recruiter.save()
        return user
