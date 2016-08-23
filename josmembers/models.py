from django.db import models
from django.contrib.auth.models import User

from mezzanine.core.models import TimeStamped
from mezzanine.utils.models import AdminThumbMixin

# Create your models here.


class JOSProfile(AdminThumbMixin, TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Member Profile'
        verbose_name_plural = 'Member Profiles'
        ordering = ("user",)

    user = models.OneToOneField(User, related_name='JOSProfile', on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True)

    about_me = models.TextField(default="Coming Soon!", null=True)

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


PRIMARY_DEVICE_CHOICES = (
    (1, 'Laptop'),
    (2, 'Desktop'),
    (3, 'Tablet'),
)

PRIMARY_OS_CHOICES = (
    (1, 'Windows'),
    (2, 'Mac'),
    (3, 'Other'),
    (4, 'Uncertain'),
)

BROWSER_CHOICES = (
    (1, 'Firefox'),
    (2, 'Internet Explorer'),
    (3, 'Chrome'),
    (4, 'Apple Safari'),
)

EMAIL_FREQ_CHOICES = (
    (1, 'More than once a day'),
    (2, 'Everyday'),
    (3, 'Rarely'),
    (4, 'Never'),
)

class JOSReservation(TimeStamped, models.Model):

    class Meta:
        verbose_name = 'Reservation'
        ordering = ("-created",)


    first_name = models.CharField(max_length=200, default=None)
    last_name = models.CharField(max_length=200, default=None)

    email = models.EmailField(default=None)

    email_frequency = models.IntegerField(default=0, choices=EMAIL_FREQ_CHOICES)
    phone = models.CharField(max_length=40, default=None)
    zip = models.CharField(max_length=10, default=None)
    phone_text = models.NullBooleanField(blank=True, default=False)

    best_time_to_call = models.TextField(default=None)

    primary_device = models.IntegerField(default=0, choices=PRIMARY_DEVICE_CHOICES)

    primary_os = models.IntegerField(default=0, choices=PRIMARY_OS_CHOICES)

    webcam = models.NullBooleanField(blank=True, default=False)
    browser = models.TextField(blank=True, default=None)
    refer = models.TextField(blank=True, null=True, default=None)
    staff_notes = models.TextField(blank=True, null=True, default=None)






