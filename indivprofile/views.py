from django.shortcuts import render,get_object_or_404
from users.models import Profile
# Create your views here.

def showprofile(request,profile_id ):
    profile = get_object_or_404(Profile, id=profile_id)
    return render(request, 'indivprofile/profile.html', {'profile': profile})
