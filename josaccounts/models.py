from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import date

from mezzanine.core.models import Ownable, Displayable
from mezzanine.core.fields import FileField
from mezzanine.utils.models import AdminThumbMixin, upload_to

# Create your models here.


class JOSProfile(AdminThumbMixin, Displayable):
    class Meta:
        verbose_name = 'JOS Member Profile'
        verbose_name_plural = 'JOS Members Profile'
        ordering = ("user",)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    date_of_birth = models.DateField(null=True, blank=True)

    about_me = models.TextField(null=True, blank=True)

    profile_photo = FileField(verbose_name=_("Profile Photo"),
                               upload_to=upload_to("josaccounts.JOSProfile.profile_photo", "josaccounts"),
                               format="Image", max_length=255, null=True, blank=True)

    admin_thumb_field = "profile_photo"

    def get_absolute_url(request):
        username = request.user.username
        return "/users/%s/" % username


