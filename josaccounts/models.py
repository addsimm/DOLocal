from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class JOSProfile(models.Model):
    class Meta:
        verbose_name = 'JOS Member Profile'
        verbose_name_plural = 'JOS Members Profile'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    join_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    background = models.TextField(null=True, blank=True)

