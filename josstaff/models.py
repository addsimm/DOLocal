from django.db import models

# Create your models here.

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.core.models import TimeStamped
from mezzanine.pages.models import Orderable, Displayable
from mezzanine.utils.models import AdminThumbMixin, upload_to

from adminsortable.models import SortableMixin



class StrippedCharField(models.CharField):
    """Newforms CharField that strips trailing and leading spaces."""
    def clean(self, value):
        if value is not None:
            value = value.strip()
        return super(StrippedCharField, self).clean(value)

class JOSStaffMember(AdminThumbMixin, Orderable, Displayable):
    ''' A model for JOS Staff Members '''

    class Meta:
        verbose_name = 'JOS Staff Member'
        verbose_name_plural = 'JOS Staff Members'

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

    start_hours = models.PositiveSmallIntegerField()

    admin_thumb_field = "bio_image"

    def user_name(self):
        un = str(self.first_name + self.last_name)
        return (un.lower())

    def __unicode__(self):
        return self.title

    def get_cumulative_hours(self):
        cumhours = JOSStaffHoursEntry.objects.filter(self).aggregate(sum('hours_claimed'))

        return cumhours


class JOSStaffHoursEntry(TimeStamped, models.Model):

    staff_member = models.ForeignKey(JOSStaffMember)
    period_date_start = models.DateField()
    period_date_end = models.DateField()
    hours_claimed = models.PositiveSmallIntegerField()
    hours_notes = models.TextField()
    time_claim_approved = models.BooleanField(default=False)
