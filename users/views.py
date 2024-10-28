from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime
from posts.models import Post, Comment
from django.contrib import messages

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
        print(username, password)
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
    

def editprofile(request):
    profile = request.user.profile
    print(profile)
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', profile.bio)
        profile.date_of_birth = request.POST.get('date_of_birth')
        
        if request.FILES.get('profile_photo'):
            profile.profile_photo = request.FILES['profile_photo']
        
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        user.save()
        profile.save()

        return redirect('show_profile', profile_id=profile.id)

    return render(request, 'users/editprofile.html',{'profile': profile})

def home(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.method == 'POST':
        if 'like_post' in request.POST:
            post_id = request.POST.get('like_post')
            post = get_object_or_404(Post, id=post_id)

            if request.user in post.likes.all():
                post.likes.remove(request.user)  
            else:
                post.likes.add(request.user)  

        elif 'comment_post' in request.POST:
            post_id = request.POST.get('comment_post')
            comment_content = request.POST.get('comment_content')
            post = get_object_or_404(Post, id=post_id)

            if comment_content:
                Comment.objects.create(
                    user=request.user,
                    post=post,
                    content=comment_content
                )
        return redirect('home')

    return render(request, 'users/home.html', {'posts': posts})

def add_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        photo = request.FILES.get('photo')
        video = request.FILES.get('video')

        # Create a new Post object
        post = Post(
            user=request.user,
            content=content,
            photo=photo if photo else None,
            video=video if video else None
        )
        post.save()

        messages.success(request, 'Your post has been added successfully!')
        return redirect('home')

    return render(request, 'users/add_post.html')
