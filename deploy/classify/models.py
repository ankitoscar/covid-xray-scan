import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=25)
    scan = models.ImageField()

    def __str__(self):
        return self.name
