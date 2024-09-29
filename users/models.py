from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='following_profiles', blank=True, symmetrical=False)
    following = models.ManyToManyField(User, related_name='follower_profiles', blank=True, symmetrical=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
