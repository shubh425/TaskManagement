from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('regular', 'Regular'),
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
        default='regular'
    )
