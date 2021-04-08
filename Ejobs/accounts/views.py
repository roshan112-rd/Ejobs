from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from jobs.models import Job

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
        image = request.FILES['image']
        
        if password1 != password2:
            messages.info(request, 'passwords are different')
            return redirect('seeker_register')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'username taken')
            return redirect('seeker_register')
           
        if User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
            return redirect('seeker_register')
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        Seeker.objects.create(user=user, contact=contact, gender=gender, address=address, image=image)
        auth.login(request, user)
                
        subject = 'welcome to EJobs'
        message = f'Hi {user.username}, thank you for registering in EJobs.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('seeker_dashboard')

    else:
        return render(request, 'seeker/seeker_register.html')

    
    

def seeker_dashboard(request):
    if request.user.is_authenticated:
        user_details = SeekerAdditionalDetails.objects.get(user=request.user) 
        jobs = Job.objects.filter(job_category=user_details.preferred_job_category)
        # jobs = Job.objects.all()

        # print(jobs[0].job_category)
        print(user_details.preferred_job_category)
        return render(request, 'seeker/seekerDashboard.html',{'jobs': jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('login')

def seeker_profile(request):
    if request.user.is_authenticated:
        userdata = Seeker.objects.filter(user=request.user)
        adddata = SeekerAdditionalDetails.objects.filter(user=request.user)
        socialdata = SeekerSocialDetails.objects.filter(user=request.user)
        return render(request, 'seeker/profile.html', {'userdata': userdata ,'adddata': adddata , 'socialdata': socialdata})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


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

        user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password1, email=email, username=username,is_staff=True)
        Recruiter.objects.create(user=user, contact=contact, address=address,company_type=company_type,company_name=company_name, image=image)
 
        auth.login(request, user)
        return redirect('recruiter_dashboard')


        subject = 'welcome to EJobs'
        message = f'Hi {user.username}, thank you for registering as recruiter in EJobs.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('seeker_dashboard')
    else:
        return render(request, 'recruiter/recruiter_register.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        user = auth.authenticate(username=username, password=password1)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            return HttpResponseRedirect('/admin/')

        elif user is not None and user.is_staff:
            auth.login(request, user)
            return redirect('recruiter_dashboard')

        elif user is not None and not user.is_staff and not user.is_superuser:
            auth.login(request, user)
            return redirect('seeker_dashboard')

    else:
        return render(request, 'seeker/login.html')
    return render(request, 'seeker/login.html')

  
def recruiter_dashboard(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(user=request.user)
        return render(request, 'recruiter/recruiterDashboard.html', {'jobs': jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('login')


def recruiter_profile(request):
    if request.user.is_authenticated:
        userdata = Recruiter.objects.filter(user=request.user)
        return render(request, 'recruiter/profile.html', {'userdata': userdata})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


def logout(request):
    auth.logout(request)
    messages.info(request, 'logged out successfully')
    return redirect('home')

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


