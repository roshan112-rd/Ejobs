from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages, auth
from .forms import *
from django.http import HttpResponseRedirect
from accounts.models import *
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
                # print(form)
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
        return render(request, 'jobs/jobhome.html', {'jobs': jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


def jobs(request):
    if request.user.is_authenticated:
        jobs = Job.objects.all()
        return render(request, 'jobs/jobs.html', {'jobs': jobs})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


def saved_jobs(request):
    if request.user.is_authenticated:
        jobs=SavedJobs.objects.filter(user=request.user)
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
    return render(request, 'jobs/applicants.html',{'jobs':jobs})



def applicant(request, job_id):
    jobs=AppliedJobs.objects.filter(job=job_id, job__user=request.user)
    if(jobs):
        job=jobs[0]
    else:
        job='sorry! no seekers found'
    return render(request, 'jobs/applicant.html',{'jobs':jobs,'job':job})


  
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

def job_details(request, id):
    if request.user.is_authenticated:
        job = Job.objects.get(job_id= id)
        return render(request, 'jobs/job_details.html', {'job': job})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')



#job details for seeker
def job_details_2(request, id):
    if request.user.is_authenticated:
        job = Job.objects.get(job_id= id)
        return render(request, 'jobs/job_details_2.html', {'job': job})
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')
        

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
                    applied_jobs=AppliedJobs(job=job,user=user,usercv=usercv)
                    applied_jobs.save()
                    messages.info(request, 'Applied successfully!')
                    return redirect('appliedJobs')
                else:
                    messages.info(request, 'Couldnot apply!')
            except:
                return redirect('appliedJobs')
    else:
        messages.info(request, 'You are not logged in. Please log in to continue')
        return redirect('home')


def search(request):
    query = request.GET['query']
    jobs = Job.objects.filter(job_title__icontains=query)
    allJob =  {'jobs': jobs}
    return render(request, 'jobs/search.html',allJob)       



def decline(request):
    return redirect('applicants') 