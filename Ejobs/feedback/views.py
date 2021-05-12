from django.shortcuts import render, redirect
from.models import *
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages, auth



# Create your views here.
def feedback(request):
    if request.method =="POST":
        email = request.POST['email']
        feedback = request.POST['feedback']

        Feedback.objects.create(email=email, feedback=feedback)
    
        subject = 'Feedback'
        message = f'hello user, thank you for your feedback.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        try:
            send_mail( subject, message, email_from, recipient_list )
        except:
            return redirect('home')
        messages.info(request, 'Thank you for your feedback.')
        return redirect('home')
        
    else:
        return render (request, 'feedback/feedback.html')


def about_us(request):
    return render (request, 'aboutUs.html')
