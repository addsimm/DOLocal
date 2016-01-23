from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class JOSProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    background = models.TextField(null=True, blank=True)

