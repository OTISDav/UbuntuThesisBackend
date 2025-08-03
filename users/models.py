from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_picture = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f'Profile de {self.user.username}'

class NotificationPreference(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    notify_on_new_theses = models.BooleanField(default=True)
    notify_on_updates = models.BooleanField(default=True)

    def __str__(self):
        return f"Notifications de {self.user.username}"
