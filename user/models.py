from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """Base user model plus unique email, phone, image, city"""
    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contacts = models.JSONField(null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


    def __str__(self):
        return self.email
