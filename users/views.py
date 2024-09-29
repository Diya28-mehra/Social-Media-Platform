from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime

def index(request):
    return render(request, 'users/main.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        dob_str = request.POST.get('date_of_birth')

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'users/register.html', {'error': 'Invalid date of birth format'})

        if password == confirm_password:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            
            Profile.objects.create(
                user=user,
                date_of_birth=dob
            )
            
            auth_login(request, user)
            print(f'User {username} created and logged in.')
            return redirect('home')
        else:
            return render(request, 'users/register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'users/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if Profile.objects.filter(user=user).exists():
                auth_login(request,user)
                print(f'User {username} logged in successfully.')
                return redirect('home')
            else:
                print(f'User profile not found for {username}')
                return render(request,'users/main.html',{'error':'User Profile Not Found'})
        else:
            print(f'Invalid username or password for {username}')
            return render(request, 'users/main.html', {'error': 'Invalid username or password'})
    return render(request, 'users/main.html')

def home(request):
    profiles = Profile.objects.order_by('user__username')
    return render(request,'users/home.html',{'profiles':profiles})

def editprofile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', profile.bio)
        profile.date_of_birth = request.POST.get('date_of_birth', profile.date_of_birth)
        
        if request.FILES.get('profile_photo'):
            profile.profile_photo = request.FILES['profile_photo']
        
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        user.save()
        profile.save()

        return redirect('profile')  
    return render(request, 'users/editprofile.html', {'profile': profile})