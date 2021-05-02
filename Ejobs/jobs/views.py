from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages, auth
from .forms import *
from django.http import HttpResponseRedirect
from accounts.models import *
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.core.paginator import Paginator


# Create your views here.
def add_job(request):
    if request.user.is_authenticated:
        form = JobForm()
        user=User.objects.get(username=request.user)
        form.fields['user'].initial  = user.id
        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                form.fields['user'] = user
                form.save()
                return redirect('jobhome')
                
            else:
                messages.info(request, 'invalid date format (mm/dd/yyyy)')
                return render(request, 'jobs/addJob.html', {'form': form})
        else:
            return render(request, 'jobs/addJob.html', {'form': form})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


def jobhome(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(user=request.user)
        paginator = Paginator(jobs, 3)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
        return render(request, 'jobs/jobhome.html', {'jobs': jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


def jobs(request):
    if request.user.is_authenticated:
        jobs = Job.objects.all()
        paginator = Paginator(jobs, 3)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
        return render(request, 'jobs/jobs.html', {'jobs': jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')

def saved_jobs(request):
    if request.user.is_authenticated:
        jobs=SavedJobs.objects.filter(user=request.user)
        paginator = Paginator(jobs, 3)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
        if(jobs):
            job=jobs[0]
        else:
            messages.info(request, 'You havent saved any jobs')
        return render(request, 'jobs/savedjobs.html',{'jobs':jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')

def appliedJobs(request):
    if request.user.is_authenticated:
        jobs=AppliedJobs.objects.filter(user=request.user)
        paginator = Paginator(jobs, 3)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
        if(jobs):
            job=jobs[0]
        else:
            messages.info(request, 'You havent applied any jobs')
        return render(request, 'jobs/appliedJobs.html',{'jobs':jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')



def applicants(request):
    jobs=Job.objects.filter(user=request.user)
    job_count = Job.objects.filter(user=request.user).count()
    applicant_count = AppliedJobs.objects.count()
    return render(request, 'jobs/applicants.html',{'jobs':jobs,'job_count':job_count,'applicant_count':applicant_count})



def applicant(request, job_id):
    jobs=AppliedJobs.objects.filter(job=job_id, job__user=request.user)
    count=AppliedJobs.objects.filter(job=job_id, job__user=request.user).count()
    if(jobs):
        job=jobs[0]
    else:
        job='sorry! no seekers found'
    return render(request, 'jobs/applicant.html',{'jobs':jobs,'job':job,'count':count})


  
def delete_job(request,id):
    obj = Job.objects.get(job_id= id)
    obj.delete()
    messages.info(request, 'job deleted')
    return redirect('jobhome')



def remove_job(request,id):
    obj = SavedJobs.objects.get(job_id= id,user=request.user)
    obj.delete()
    messages.info(request, 'job removed')
    return redirect('saved_jobs')



def remove_applied_job(request,id):
    obj = AppliedJobs.objects.get(job_id= id)
    obj.delete()
    messages.info(request, 'job removed')
    return redirect('appliedJobs')



def save_job(request,job_id):
    if request.user.is_authenticated:
        if SavedJobs.objects.filter(job_id=job_id,user=request.user).exists():
                messages.info(request, 'you already saved this job')
                return redirect('saved_jobs')
        else:
            if request.user.is_authenticated:
                try:
                    job=Job.objects.get(job_id=job_id)
                    user=User.objects.get(username=request.user)
                    saved_Jobs=SavedJobs(job=job,user=user)
                    saved_Jobs.save()
                    return redirect('saved_jobs')
                except:
                    return redirect('saved_jobs')
    
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')

def job_details(request, id):
    if request.user.is_authenticated:
        job = Job.objects.get(job_id= id)
        return render(request, 'jobs/job_details.html', {'job': job})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')



#job details for seeker
def job_details_2(request, id):
    if request.user.is_authenticated and request.user.is_staff:
        messages.info(request, 'You dont have access to this page')
        return redirect('home')
    # elif request.user.is_authenticated:
    #     job = Job.objects.get(job_id= id)
    #     return render(request, 'jobs/job_details_2.html', {'job': job})
    else:
        job = Job.objects.get(job_id= id)
        return render(request, 'jobs/job_details_2.html', {'job': job})
        # messages.info(request, 'You are not logged in. Please log in to continue')
        # return redirect('home')
        

def apply_job(request,job_id):
    if request.user.is_authenticated:
        if AppliedJobs.objects.filter(job_id=job_id,user=request.user).exists():
                messages.info(request, 'you already applied for this job')
                return redirect('appliedJobs')
        else:            
            try:
                if request.method == "POST":
                    job=Job.objects.get(job_id=job_id)
                    user=User.objects.get(username=request.user)
                    usercv=request.FILES.get('usercv')
                    applied_jobs=AppliedJobs(job=job,user=user,usercv=usercv)
                    applied_jobs.save()
                    messages.info(request, 'Applied successfully!')
                    return redirect('appliedJobs')
                else:
                    messages.info(request, 'Couldnot apply!')
                    return redirect('appliedJobs')
            except:
                return redirect('appliedJobs')
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


def search(request):

    query = request.GET['query']
    if(query==''):
        return redirect("jobs")
    jobs = Job.objects.filter(Q(job_title__icontains=query) | Q(job_employer__icontains=query) | Q(job_position__icontains=query) | Q(job_category__icontains=query))
    if (jobs):
        allJob =  {'searched_jobs': jobs}
        return render(request, 'jobs/jobs.html',allJob)
    else:
        messages.info(request, 'job not found')
        return redirect('jobs')






def decline(request,id):
    try:
        job= AppliedJobs.objects.get(id=id)
        email=job.user.email
        name=job.user.first_name
        job_title=job.job.job_title
        send_mail(
        'Job application DECLINED',
        f'''
        dear {name}, we are sorry to inform you that your job application for({job_title}) has been declined.
        ''',
        'hello.ejobs@gmail.com',
        [f'{email}',],
        fail_silently=True,)
        job.delete()
        return redirect('applicants')
    finally:
        messages.info(request, 'cannot decline job')



def accept(request,id):
    job= AppliedJobs.objects.get(id=id)
    email=job.user.email
    name=job.user.first_name
    job_title=job.job.job_title
    send_mail(
    'Job application ACCEPTED',
    f'''
    dear {name},your job application for({job_title}) has been accepted. You will recieve calls or messages from the recruiter regarding further processing.
    ''',
    'hello.ejobs@gmail.com',
    [f'{email}',],
    fail_silently=True,)
    job.delete()
    return redirect('applicants') 



def edit_method(request,job_id,model,cls):
    job= get_object_or_404(model,job_id=job_id)
    if request.method =="POST":
        form = cls(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobhome')

    else:
        form = cls(instance=job)
        return render(request, 'jobs/edit_job.html', {'form': form})

def edit_job(request,job_id):
    return edit_method(request,job_id,Job,JobForm)





        