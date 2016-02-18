from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import TimeStamped
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.utils.models import AdminThumbMixin, upload_to


# Create your models here.


class JOSProfile(AdminThumbMixin, TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Member Profile'
        verbose_name_plural = 'JOS Members Profile'
        ordering = ("user",)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(null=True, blank=True)

    about_me = RichTextField(null=True, blank=True)

    profile_photo = FileField(verbose_name=_("Profile Photo"),
                            upload_to=upload_to("josmembers.JOSProfile.profile_photo", "josmembers"),
                            format="Image", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(request):
        username = request.user.username
        return "/users/%s/" % username