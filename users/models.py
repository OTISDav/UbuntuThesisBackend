from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

User = get_user_model()

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notify_on_new_theses = models.BooleanField(default=True)
    notify_on_updates = models.BooleanField(default=True)

    def __str__(self):
        return f"Notifications de {self.user.username}"
