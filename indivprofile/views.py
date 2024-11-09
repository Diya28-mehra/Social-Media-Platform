from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User
from posts.models import Post
from django.shortcuts import redirect

# Create your views here.

@login_required 
def showprofile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    return render(request, 'indivprofile/profile.html', {
        'profile': profile,
        'posts': posts,
    })

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('show_profile', user_id=request.user.id)

