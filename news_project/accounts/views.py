from django.shortcuts import render, redirect

# Create your views here.
from .models import Subscriber
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            sub, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Thanks — you are subscribed!')
                return redirect('accounts:success')
            else:
                messages.info(request, 'You are already subscribed.')
                return redirect('accounts:success')
    return render(request, 'accounts/signup.html')

def success(request):
    return render(request, 'accounts/success.html')