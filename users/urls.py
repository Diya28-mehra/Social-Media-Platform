from django.urls import path
from .views import index,register,home,editprofile
from indivprofile.views import showprofile

urlpatterns = [
    path('',index,name='main'),
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('profile/<int:profile_id>/',showprofile,name='show_profile'),
    path('edit-profile/',editprofile,name='edit_profile'),
]
