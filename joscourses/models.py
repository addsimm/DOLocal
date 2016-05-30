from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from mezzanine.core.models import TimeStamped

from ckeditor.fields import RichTextField
from embed_video.fields import EmbedVideoField


# Create your models here.


class JOSCourse(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Course'
        ordering = ("semester",)

    course_title = models.CharField(max_length=150, default="untitled")
    courseno = models.IntegerField(default=0)
    description = RichTextField(default="coming soon")
    instructor = models.ForeignKey(User, related_name="instructor_user")
    location = models.CharField(max_length=150, default="tbd")

    semester = models.IntegerField(default=1)
    weeks = models.IntegerField(default=8)

    start_date = models.DateTimeField(blank=True)
    repeat_period = models.IntegerField(default=7)
    end_date = models.DateTimeField(blank=True)

    publish = models.BooleanField(default=False)

    students = models.ManyToManyField(User, related_name="student_users", through='JOSCourseStudent')

    def __unicode__(self):
        return 'Course: ' + self.course_title


class JOSCourseStudent(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Course Student'
        ordering = ("course",)
        unique_together = ('student', 'course')

    student = models.ForeignKey(User)
    course = models.ForeignKey(JOSCourse)

    def __unicode__(self):
        return 'Enrollee: ' + self.student.JOSProfile.jos_name()


class JOSCourseWeek(TimeStamped, models.Model):
    week_title = models.CharField(max_length=150, default="untitled")
    weekno = models.IntegerField(default=0)
    course = models.ForeignKey(JOSCourse)
    video = EmbedVideoField(blank=True)  # same like models.URLField()
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Week #' + str(self.weekno) + ": " + self.week_title


class JOSHandout(TimeStamped, models.Model):
    courseweek = models.ForeignKey(JOSCourseWeek)
    handout_title = models.CharField(max_length=150, default="untitled")
    handoutno = models.IntegerField(default=0)
    content = RichTextField(default="coming soon")
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Handout #' + str(self.handoutno) + ": " + self.handout_title

class JOSStoryActivity(TimeStamped, models.Model):
    courseweek = models.ForeignKey(JOSCourseWeek)
    activity_title = models.CharField(max_length=150, default="untitled")
    activityno = models.IntegerField(default=0)
    content = RichTextField(default="coming soon")
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Activity #' + str(self.activityno) + ": " + self.activity_title
