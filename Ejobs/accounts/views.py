from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from jobs.models import Job


# register method for seeker
def seeker_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        username = request.POST['username']
        
        contact = request.POST['contact']
        gender = request.POST['gender']
        address = request.POST['address']
        bio = request.POST['bio']
        image = request.FILES['image']
        
        if password1 != password2:
            messages.info(request, 'passwords are different')
            return redirect('seeker_register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'username taken')
            return redirect('seeker_register')
           
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        Seeker.objects.create(user=user, contact=contact, gender=gender, address=address, image=image, bio=bio)
        auth.login(request, user)
        
        # sending mail after user creation      
        subject = 'welcome to EJobs'
        message = f'Hi {user.username}, thank you for registering in EJobs.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        try:
            send_mail( subject, message, email_from, recipient_list )
        except:
            return redirect('seeker_dashboard')
        return redirect('seeker_dashboard')
    else:
        return render(request, 'seeker/seeker_register.html')


# recruiter registration
def recruiter_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        username = request.POST['username']
        
        contact = request.POST['contact']
        address = request.POST['address']
        company_type=request.POST['company_type']
        company_name=request.POST['company_name']
        bio = request.POST['bio']
        website = request.POST['website']
        image = request.FILES['image']

        if password1 != password2:
            messages.info(request, 'passwords are different')
            return redirect('recruiter_register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'username taken')
            return redirect('recruiter_register')
           
        if User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
            return redirect('recruiter_register')
        # assigning staff status to recruiters
        user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password1, email=email, username=username,is_staff=True)
        Recruiter.objects.create(user=user, contact=contact, address=address,company_type=company_type,company_name=company_name, image=image, bio=bio, website=website)
 
        auth.login(request, user)
        return redirect('recruiter_dashboard')

        # sending mail after user creation 
        subject = 'welcome to EJobs'
        message = f'Hi {user.username}, thank you for registering as recruiter in EJobs.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        try:
            send_mail( subject, message, email_from, recipient_list )
        except:
            return redirect('recruiter_dashboard')
        return redirect('recruiter_dashboard')
    else:
        return render(request, 'recruiter/recruiter_register.html')


# logging in by checking staff status of user
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        user = auth.authenticate(username=username, password=password1)
        # superusers will be redirected into admin panel
        if user is not None and user.is_superuser:
            auth.login(request, user)
            return HttpResponseRedirect('/admin/')

        # staff status user will be redirected to recruiter dashboard
        elif user is not None and user.is_staff:
            auth.login(request, user)
            return redirect('recruiter_dashboard')

        # rest of the users will be redirected to seeker dashboard
        elif user is not None and not user.is_staff and not user.is_superuser:
            auth.login(request, user)
            return redirect('seeker_dashboard')
    else:
        return render(request, 'seeker/login.html')
    return render(request, 'seeker/login.html')

# dashboard for seekers
def seeker_dashboard(request):
    if request.user.is_authenticated:
        try:
            user_details = SeekerAdditionalDetails.objects.get(user=request.user) 
            jobs = Job.objects.filter(job_category=user_details.preferred_job_category)
            return render(request, 'seeker/seekerDashboard.html',{'jobs': jobs})
        except:
            return render(request, 'seeker/seekerDashboard.html')
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('login')


# dashboard for recruiter
def recruiter_dashboard(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(user=request.user)
        return render(request, 'recruiter/recruiterDashboard.html', {'jobs': jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('login')


#return redirect('home')combined profile method for both seeker and recruiter
def profile(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_staff:
            userdata = Recruiter.objects.filter(user=request.user)
            return render(request, 'recruiter/profile.html', {'userdata': userdata})
        else:
            userdata = Seeker.objects.filter(user=request.user)
            adddata = SeekerAdditionalDetails.objects.filter(user=request.user)
            socialdata = SeekerSocialDetails.objects.filter(user=request.user)
            return render(request, 'seeker/profile.html', {'userdata': userdata ,'adddata': adddata , 'socialdata': socialdata})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


# logout function
def logout(request):
    auth.logout(request)
    messages.info(request, 'logged out successfully')
    return redirect('home')


# additional details of the seeker
def additional_details(request):
    if request.method == 'POST':
        university = request.POST['university']
        qualification = request.POST['qualification']
        skills = request.POST['skills']
        preferred_job_category = request.POST['preferred_job_category']
        available_for = request.POST['available_for']
        preferred_location = request.POST['preferred_location']
        work_experience = request.POST['work_experience']

        user=User.objects.get(username=request.user)
        SeekerAdditionalDetails.objects.create(user=user, qualification=qualification, university=university, skills=skills, preferred_job_category=preferred_job_category, available_for=available_for,preferred_location=preferred_location,work_experience=work_experience )
        return redirect('seeker_profile')
    else:
        return render(request, 'seeker/additional_details.html')


# social details of the seeker
def social_details(request):
    if request.method == 'POST':
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        twitter = request.POST['twitter']
        others = request.POST['others']

        user=User.objects.get(username=request.user)
        SeekerSocialDetails.objects.create(user=user, facebook=facebook, instagram=instagram, twitter=twitter, others=others)
        return redirect('seeker_profile')
    else:
        return render(request, 'seeker/social_details.html')