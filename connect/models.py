from django.db import models
from users.models import Profile
# Create your models here.
class FriendRequest(models.Model):
    from_user = models.ForeignKey(Profile, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='friend_requests_received', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friend request from {self.from_user.user.username} to {self.to_user.user.username}"

class Friend(models.Model):
    user1 = models.ForeignKey(Profile, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Profile, related_name='friend2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user1.user.username} and {self.user2.user.username} are friends'
