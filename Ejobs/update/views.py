from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from jobs.models import Job
from accounts.models import *
# Create your views here.

def password_change(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            password1=request.POST.get('password1')
            password2=request.POST.get('password2')
            user=request.user

            if(password1 == password2):
                user.set_password(password1)
                user.save()

                subject = 'welcome to EJobs'
                message = f'Hi {user.username}, your password has been changed successfully.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                try:
                    send_mail( subject, message, email_from, recipient_list )
                except:
                    return redirect('home')
                
                messages.info(request, 'password changed successfully. Please login again to continue.')
                return redirect('home')

            
            else:
                messages.info(request, 'password is different')
                return redirect('password_change')

            
        else:
            return render(request, 'change_password.html')
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')

def edit_add_details(request):
    if request.method == 'POST':
        university = request.POST['university']
        qualification = request.POST['qualification']
        skills = request.POST['skills']
        
        available_for = request.POST['available_for']
        preferred_location = request.POST['preferred_location']
        work_experience = request.POST['work_experience']
        user=User.objects.get(username=request.user)
        adddata = SeekerAdditionalDetails.objects.filter(user=request.user)[0]
       

        adddata.qualification=qualification
        adddata.university=university
        adddata.skills=skills
        adddata.available_for=available_for
        adddata.referred_location=preferred_location
        adddata.work_experience=work_experience
    
        adddata.save()
        return redirect('profile')
    else:
        adddata = SeekerAdditionalDetails.objects.filter(user=request.user)[0]
        return render(request,'seeker/edit_add_details.html', {"adddata":adddata})

def edit_social_data(request):
    if request.method == 'POST':
        facebook = request.POST['facebook']
        instagram = request.POST['instagram']
        twitter = request.POST['twitter']
        others = request.POST['others']
        
        user=User.objects.get(username=request.user)
        social_data = SeekerSocialDetails.objects.filter(user=request.user)[0]

        social_data.facebook=facebook
        social_data.instagram=instagram
        social_data.twitter=twitter
        social_data.others=others

        social_data.save()
        return redirect('profile')

    else:
        social_data = SeekerSocialDetails.objects.filter(user=request.user)[0]
        return render(request,'seeker/edit_social_details.html', {"social_data":social_data})

def edit_user_data(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        contact = request.POST['contact']
        preferred_job_category = request.POST['preferred_job_category']
        gender = request.POST['gender']
        address = request.POST['address']
        bio = request.POST['bio']
        # image = request.FILES['image']

        user=request.user

        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        
        user.save()



        user=User.objects.get(username=request.user)
        user_data = Seeker.objects.filter(user=request.user)[0]
        user_data.preferred_job_category=preferred_job_category
        user_data.contact=contact
        user_data.gender=gender
        user_data.address=address
        user_data.bio=bio
        # user_data.image=image
        user_data.save()
        return redirect('profile')

    else:
        user_data = Seeker.objects.filter(user=request.user)[0]
        return render(request,'seeker/edit_user.html', {"user_data":user_data})

def edit_recruiter_data(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        
        contact = request.POST['contact']
        address = request.POST['address']
        company_type=request.POST['company_type']
        company_name=request.POST['company_name']
        bio = request.POST['bio']
        website = request.POST['website']
        # image = request.FILES['image']
       
        user=request.user
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()



        user=User.objects.get(username=request.user)
        rec_data = Recruiter.objects.filter(user=request.user)[0]

        rec_data.contact=contact
        rec_data.company_type=company_type
        rec_data.address=address
        rec_data.bio=bio
        # rec_data.image=image
        rec_data.company_name=company_name
        rec_data.website=website
        rec_data.save()
        return redirect('profile')

    else:
        rec_data = Recruiter.objects.filter(user=request.user)[0]
        return render(request,'recruiter/edit_recruiter_data.html', {"rec_data":rec_data})

def pp_change(request):
    if request.method =='POST':
        image = request.FILES['image']
        user=User.objects.get(username=request.user)
        if user.is_staff:
            img = Recruiter.objects.filter(user=request.user)[0]
        else:
            img = Seeker.objects.filter(user=request.user)[0]
        img.image=image
        img.save()
        return redirect('profile')
    else:
        return render(request,'recruiter/profile.html')


def change_pp(request):
    if request.method =='POST':
        image = request.FILES['image']
        user=User.objects.get(username=request.user)

        img = Seeker.objects.filter(user=request.user)[0]
        img.image=image
        img.save()
        return redirect('profile')
    else:
        return render(request,'seeker/profile.html')


def remove_social(request):
    if request.user.is_authenticated:
        social = SeekerSocialDetails.objects.get(user=request.user)
        social.delete()
        messages.info(request, 'Social data removed ')
        return redirect('profile')
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')






def remove_add(request):
    if request.user.is_authenticated:
        social = SeekerAdditionalDetails.objects.get(user=request.user)
        social.delete()
        messages.info(request, 'Additional data removed ')
        return redirect('profile')

    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')