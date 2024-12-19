from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('regular', 'Regular'),
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
        default='regular'
    )

class Task(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    task_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.task_name