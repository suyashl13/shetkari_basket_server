from django.db import models


# Create your models here.
class Announcement(models.Model):
    announcement = models.CharField(max_length=255)
    type = models.CharField(max_length=12)
    date_created = models.DateTimeField(auto_now=True)