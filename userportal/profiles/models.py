from django.db import models


class User(models.Model):

    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    bio = models.CharField(max_length=200)

    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} Profile"


class Settings(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    theme = models.CharField(max_length=20)

    notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Settings"