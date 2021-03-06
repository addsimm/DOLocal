from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from mezzanine.core.models import TimeStamped
from mezzanine.utils.models import AdminThumbMixin

# Create your models here.

PRIMARY_DEVICE_CHOICES=((1,'Laptop'),(2,'Desktop'),(3,'Tablet'),)
PRIMARY_OS_CHOICES=((1,'Windows'),(2,'Mac'),(3,'Other'),(4,'Uncertain'),)
BROWSER_CHOICES=((1,'Firefox'),(2,'Internet Explorer'),(3,'Chrome'),(4,'Apple Safari'),)
EMAIL_FREQ_CHOICES=((1,'Everyday'),(2,'Rarely'),(3,'Never'),)
REFER_STATUS_CHOICES=((0,'None'),(1,'Emailed'),(2,'Called'),(3,'Talked'),(4,'Webcam'),(5,'Enrolled'))

NONE,PLOT,CHARACTER,THEME,WORLD,CONFLICT=0,1,2,3,4,5
WELCOME,WHEEL,DRAFT,REVISION,SHARE=1,2,3,4,5

STORY_EL_CHOICES=((NONE,'None'),(PLOT,'Plot'),(CHARACTER,'Character'),
                 (THEME,'Theme'),(WORLD,'World'),(CONFLICT,'Conflict'))
SEVEN_DAY_PROGRESS_CHOICES=((NONE,'None'),(WELCOME,'Welcome'),(WHEEL,'Wheel'),
                            (DRAFT,'Draft'),(REVISION,'Revision'),(SHARE,'Share'))

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

        members = JOSProfile.objects.values_list('user').filter(teams=self).order_by('-user')

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

    seven_day_progress = models.IntegerField(default=NONE, choices=STORY_EL_CHOICES)

    seven_day_els_complete = ArrayField(models.IntegerField(
            default=NONE, choices=STORY_EL_CHOICES), default=[0,0,0,0,0], size=5)

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

    def friendly_jos_name(request):
        first_name = request.user.get_short_name()[:8]
        last_initial = request.user.last_name[:1].upper()
        friendly_jos_name = first_name + " " + last_initial + "."
        return friendly_jos_name

    def get_teams(self):
        return ", ".join(team.name for team in self.teams.all())

    def has_teams(self):
        if len(self.get_teams()) > 0:
            return True


class JOSUserCreatedNote(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'User Created Note'

    note_text = models.TextField(default="Enter notes here", null=True)
    profile = models.ForeignKey(JOSProfile, null=True)


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
    phone_text = models.NullBooleanField(blank=True, null=True, default=False)

    best_time_to_call = models.TextField(default=None)

    primary_device = models.IntegerField(default=0, choices=PRIMARY_DEVICE_CHOICES)

    primary_os = models.IntegerField(default=0, choices=PRIMARY_OS_CHOICES)

    webcam = models.NullBooleanField(blank=True, default=False)
    printer = models.NullBooleanField(blank=True, default=False)
    browser = models.TextField(blank=True, default=None)
    refer = models.TextField(blank=True, null=True, default=None)

    staff_notes = models.TextField(blank=True, null=True, default=None)
    status = models.IntegerField(default=0, choices=REFER_STATUS_CHOICES)