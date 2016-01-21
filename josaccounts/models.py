from django.db import models

# Create your models here.


class JOSProfile(models.Model):
    user = models.OneToOneField("auth.User")
    date_of_birth = models.DateField()
    bio = models.TextField()
    chunky = models.TextField()
