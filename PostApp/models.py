from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    caption = models.TextField(max_length=264, blank=True)
    image = models.ImageField(upload_to='post_images')
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-upload_date']

class Like(models.Model):
    post =  models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker')
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user, self.post}'


