from django.urls import path
from .views import index,register,home,editprofile, login,add_post,logout
from indivprofile.views import showprofile,delete_post
from connect.views import connect_with_friends
urlpatterns = [
    path('',index,name='main'),
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('profile/<int:user_id>/',showprofile,name='show_profile'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('edit-profile/',editprofile,name='edit_profile'),
    path('login', login, name="login"),
    path('logout',logout,name='logout'),
    path('connect-with-friends',connect_with_friends,name='connect_with_friends'),
    path('add-post/',add_post, name='add_post'),
]
