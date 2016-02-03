from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.pages.models import Displayable
from mezzanine.utils.models import AdminThumbMixin, upload_to

from adminsortable.models import SortableMixin



class StrippedCharField(models.CharField):
    """Newforms CharField that strips trailing and leading spaces."""
    def clean(self, value):
        if value is not None:
            value = value.strip()
        return super(StrippedCharField, self).clean(value)

class JOSStaffMember(SortableMixin, AdminThumbMixin, Displayable):
    ''' A model for JOS Staff Members '''

    class Meta:
        verbose_name = 'JOS Staff Member'
        verbose_name_plural = 'JOS Staff Members'
        ordering = ['the_order']

    # define the field the model should be ordered by
    the_order = models.PositiveIntegerField(default=0, editable=True)

    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    jos_title = models.CharField(max_length=60, blank=True)
    email = models.EmailField(blank=True)
    bio_text = models.TextField(blank=True)
    bio_image = FileField(verbose_name=_("Bio Image"),
                               upload_to=upload_to("josstaff.staffgallery.bio_image", "josstaff"),
                               format="Image", max_length=255, null=True, blank=True)

    admin_thumb_field = "bio_image"


    def user_name(self):
        un = str(self.first_name + self.last_name)
        return (un.lower())

    def __unicode__(self):
        return self.title