from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=38)
    email = models.EmailField(max_length=200)
    phone = models.CharField(unique=True, max_length=12)
    address = models.TextField(max_length=255, default="")

    USERNAME_FIELD = 'phone'
    auth_token = models.CharField(max_length=10)
    REQUIRED_FIELDS = ['address']

    def __str__(self):
        return f"{self.name} ({str(self.phone)})"
