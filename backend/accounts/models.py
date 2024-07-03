from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null = True, blank = True)
    USER_TYPES = (
        ('regular', 'Regular User'),
        ('admin', 'Admin'),
    )

    def __str__(self):
        return f"{self.username} {self.email}"
