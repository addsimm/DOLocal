from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.pages.models import Displayable
from mezzanine.utils.models import AdminThumbMixin, upload_to


class StrippedCharField(models.CharField):
    """Newforms CharField that strips trailing and leading spaces."""
    def clean(self, value):
        if value is not None:
            value = value.strip()
        return super(StrippedCharField, self).clean(value)

class JOSStaffMember(AdminThumbMixin, Displayable):
    '''
    A model for JOS Staff Members
    '''
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    first_name =StrippedCharField(max_length=60)
    last_name = StrippedCharField(max_length=60)
    email = models.EmailField(blank=True)
    bio_text = models.TextField(blank=True)
    bio_image = FileField(verbose_name=_("Bio Image"),
                               upload_to=upload_to("josstaff.staffgallery.bio_image", "josstaff"),
                               format="Image", max_length=255, null=True, blank=True)

    admin_thumb_field = "bio_image"

    def user_name(self):
        un = str(self.first_name + self.last_name)
        return (un.lower())


    class Meta:
        verbose_name = _("JOS Staff Member")
        verbose_name_plural = _("JOS Staff Members")
