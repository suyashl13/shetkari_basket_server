from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=38)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.IntegerField(unique=True)

    USERNAME_FIELD = 'phone'
    auth_token = models.CharField(max_length=10)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name + " (" + str(self.phone) + ")"