from django.db import models
from django.contrib.auth.models import User

from mezzanine.core.models import TimeStamped
from mezzanine.utils.models import AdminThumbMixin

# Create your models here.

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

STATUS_CHOICES = (
    (0, 'None'),
    (1, 'Emailed'),
    (2, 'Called'),
    (3, 'Talked'),
    (4, 'Webcam'),
    (5, 'Enrolled'),
)


class JOSTeam(TimeStamped, models.Model):
    """
    add team profile

    add team stories
    """

    class Meta:
        verbose_name = 'Team'
        ordering = ("name",)

    name = models.CharField(max_length=250, default='missing')
    description = models.CharField(max_length=250, default='missing')

    def __str__(self):
        return self.name

    def email_team(self):
        pass

    def member_id_list(self):

        members = JOSProfile.objects.values_list('user').filter(teams=self)

        member_id_list = []
        for item in members:
            member_id_list.append(item[0])

        return member_id_list

class JOSProfile(AdminThumbMixin, TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Member Profile'
        verbose_name_plural = 'Member Profiles'
        ordering = ("user",)

    user = models.OneToOneField(User, related_name='JOSProfile', on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True)

    about_me = models.TextField(default="Coming Soon!", null=True)

    profile_image_id_str = models.CharField(max_length=150, default="noimage1")

    teams = models.ManyToManyField(JOSTeam)

    def __str__(self):
        return self.user.username

    def get_absolute_url(request):
        username = request.user.username
        return "/users/%s/" % username

    def jos_name(request):
        first_name = request.user.get_short_name()[:8]
        last_initial = request.user.last_name[:1].upper()
        jos_name = first_name + "_" + last_initial
        return jos_name


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
    printer = models.NullBooleanField(blank=True, default=False)
    browser = models.TextField(blank=True, default=None)
    refer = models.TextField(blank=True, null=True, default=None)

    staff_notes = models.TextField(blank=True, null=True, default=None)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)