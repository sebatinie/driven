import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN='ADMIN', 'Admin'
        MANAGER='MANAGER', 'Manager'
        EMPLOYEE='EMPLOYEE', 'Employee'

    role = models.CharField(
            max_length=20,
            choices=Role.choices,
            default=Role.EMPLOYEE
        )
    department = models.CharField(
        max_length=100,
        blank=True
    )
def generate_key():
        return secrets.token_urlsafe(32)
    

class APIKey(models.Model):          # used later for the custom scheme
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    key = models.CharField(max_length=64, unique=True, default=generate_key)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} key"