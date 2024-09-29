from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True, null=True)  # Allow posts to be just photos or videos with no text
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # Users who liked the post
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f'Post by {self.user.username} on {self.created_at}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'
