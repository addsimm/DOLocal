from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class JOSProfile(models.Model):
    class Meta:
        verbose_name = 'JOS Member Profile'
        verbose_name_plural = 'JOS Members Profile'
        ordering = ("user",)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    join_date = models.DateField(default=date.today)
    modified_date = models.DateTimeField(auto_now=True)
    agree_to_terms = models.BooleanField(required=True)

    about_me = models.TextField(null=True, blank=True)

