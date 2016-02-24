from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import TimeStamped
from mezzanine.core.fields import RichTextField
from mezzanine.utils.models import AdminThumbMixin

from cloudinary.models import CloudinaryField

# Create your models here.


class JOSProfile(AdminThumbMixin, TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Member Profile'
        verbose_name_plural = 'JOS Members Profile'
        ordering = ("user",)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True)

    about_me = RichTextField(default="Coming Soon!", null=True)

    profile_photo = CloudinaryField('profile photo', blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(request):
        username = request.user.username
        return "/users/%s/" % username