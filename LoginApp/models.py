from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    full_name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    dob = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    x = models.URLField(blank=True, null=True)
    description = models.TextField(max_length=350, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_date = models.DateTimeField(auto_now_add=True)
    