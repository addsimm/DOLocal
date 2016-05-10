from django.db import models
from django.contrib.auth.models import User

from mezzanine.core.models import TimeStamped
from ckeditor.fields import RichTextField
from mezzanine.utils.models import AdminThumbMixin

from pybb.profiles import PybbProfile

# Create your models here.


class JOSProfile(AdminThumbMixin, TimeStamped, PybbProfile, models.Model):
    class Meta:
        verbose_name = 'JOS Member Profile'
        verbose_name_plural = 'JOS Members Profile'
        ordering = ("user",)

    user = models.OneToOneField(User, related_name='JOSProfile', on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True)

    about_me = RichTextField(default="Coming Soon!", null=True)

    profile_image_idstr = models.CharField(max_length=150, default="noimage1")

    def __str__(self):
        return self.user.username

    def get_absolute_url(request):
        username = request.user.username
        return "/users/%s/" % username

    def jos_name(request):
        first_name = request.user.get_short_name()[:8]
        last_initial = request.user.last_name[:1].upper()
        jos_name = first_name + " " + last_initial + "."
        return jos_name


