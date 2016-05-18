from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from mezzanine.core.models import TimeStamped

from ckeditor.fields import RichTextField

# Create your models here.

class JOSCourse(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Course'
        ordering = ("title",)

    title = models.CharField(max_length=150, default="untitled")
    description = RichTextField(default="coming soon")
    semester = models.IntegerField()
    weeks = models.IntegerField()
    instructor = models.ForeignKey(User)
    location = models.CharField(max_length=150, default="tbd")
    slot = models.DateTimeField(default=datetime.now())
    students = models.ManyToManyField(User, through=JOSCourseStudent)


class JOSCourseStudent(TimeStamped, models.Model):
    student = models.ForeignKey(User)
    course = models.ForeignKey(JOSCourse)

    class Meta:
        unique_together = ('student', 'course')


class JOSCourseWeek(TimeStamped, models.Model):
    course = models.ForeignKey(JOSCourse)
    videoTranscript = RichTextField(default="coming soon")


class JOSHandout(TimeStamped, models.Model):
    courseweek = models.ForeignKey(JOSCourseWeek)
    title = models.CharField(max_length=150, default="untitled")
    content = RichTextField(default="coming soon")