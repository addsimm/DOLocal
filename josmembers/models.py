from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import TimeStamped
from ckeditor.fields import RichTextField
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

    profile_image = CloudinaryField('image', blank=True)

    profile_image_idstr = models.CharField(max_length=150, default="noimage1")

    def __str__(self):
        return self.user.username

    def get_absolute_url(request):
        username = request.user.username
        return "/users/%s/" % username


class CKRichTextHolder(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'CK Rich Text Holder'

    author = models.ForeignKey(User)
    title = models.CharField(max_length=150, default="notitle")
    field_to_edit = models.CharField(max_length=150, default="nofield")
    content = RichTextField()

