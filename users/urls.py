from django.urls import path
from .views import index,register,home,editprofile, login,add_post
from indivprofile.views import showprofile
from connect.views import connect_with_friends
urlpatterns = [
    path('',index,name='main'),
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('profile/<int:profile_id>/',showprofile,name='show_profile'),
    path('edit-profile/',editprofile,name='edit_profile'),
    path('login', login, name="login"),
    path('connect-with-friends',connect_with_friends,name='connect_with_friends'),
    path('add-post/',add_post, name='add_post'),
]
