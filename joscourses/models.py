from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from mezzanine.core.models import TimeStamped

from ckeditor.fields import RichTextField

# Create your models here.


class JOSCourse(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Course'
        ordering = ("semester",)

    course_title = models.CharField(max_length=150, default="untitled")
    description = RichTextField(default="coming soon")
    instructor = models.ForeignKey(User, related_name="instructor_user")
    location = models.CharField(max_length=150, default="tbd")

    semester = models.IntegerField(default=1)
    weeks = models.IntegerField(default=8)

    start_date = models.DateTimeField(default=datetime.now())
    repeat_period = models.IntegerField(default=7)
    end_date = models.DateTimeField(default=datetime.now())

    students = models.ManyToManyField(User, related_name="student_users", through='JOSCourseStudent')


class JOSCourseStudent(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Course Student'
        ordering = ("course",)
        unique_together = ('student', 'course')

    student = models.ForeignKey(User)
    course = models.ForeignKey(JOSCourse)


class JOSCourseWeek(TimeStamped, models.Model):
    week_title = models.CharField(max_length=150, default="untitled")
    course = models.ForeignKey(JOSCourse)
    video = models.CharField(max_length=150, default="tbd")
    videoTranscript = RichTextField(default="coming soon")


class JOSHandout(TimeStamped, models.Model):
    courseweek = models.ForeignKey(JOSCourseWeek)
    handout_title = models.CharField(max_length=150, default="untitled")
    content = RichTextField(default="coming soon")


class JOSStoryActivity(TimeStamped, models.Model):
    courseweek = models.ForeignKey(JOSCourseWeek)
    activity_title = models.CharField(max_length=150, default="untitled")
    content = RichTextField(default="coming soon")

