from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError

from .models import User

# Create your views here.
def index(request):
    return render(request, 'cards/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'cards/login.html', {
                'error': 'Wrong Username and/or Password'
            })
    return render(request, 'cards/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirmation = request.POST['password-repeat']
        email = request.POST['email']
        
        # See if passwords match
        if confirmation != password:
            return render(request, 'cards/register.html', {
                'error': 'Passwords must match'
            })
        
        # Try to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'cards/register.html', {
                'error': 'Username already taken'
            })
            
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'cards/register.html')