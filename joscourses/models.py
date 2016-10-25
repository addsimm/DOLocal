from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from mezzanine.core.models import TimeStamped
# from mezzanine.core.fields import FileField

from mezzanine.utils.models import upload_to

from embed_video.fields import EmbedVideoField

# Create your models here.

class JOSCourse(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Course'
        ordering = ("semester",)

    course_title = models.CharField(max_length=150, default="untitled")
    courseno = models.IntegerField(default=0)
    description = models.TextField(default="coming soon")
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
        verbose_name = 'Course Student'
        ordering = ("course",)
        unique_together = ('student', 'course')

    student = models.ForeignKey(User)
    course = models.ForeignKey(JOSCourse)

    def __unicode__(self):
        return 'Enrollee: ' + self.student.JOSProfile.jos_name()

class JOSCourseWeek(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Courseweek'
        ordering = ("course", "week_no")

    course = models.ForeignKey(JOSCourse)

    week_no = models.IntegerField(default=0)
    week_title = models.CharField(max_length=150, default="untitled")
    icon_name = models.CharField(max_length=150, default="missing")

    video = EmbedVideoField(blank=True)
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.week_no) + ": " + self.week_title


class JOSStoryActivity(TimeStamped, models.Model):
    courseweek = models.ForeignKey(JOSCourseWeek)
    activity_title = models.CharField(max_length=150, default="untitled")
    activityno = models.IntegerField(default=0)
    content = models.TextField(default="coming soon")
    publish = models.BooleanField(default=False)

    def __unicode__(self):
        return 'Activity #' + str(self.activityno) + ": " + self.activity_title


class JOSHandout(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Handout'
        ordering = ("courseweek", "element_order")

    PART_CHOICES = (
        (1, "Part 1"),
        (2, "Part 2"),
        (9, "Other"),
    )

    SEGMENT_CHOICES = (
        (0, "Agenda"),
        (1, "Workshop"),
        (2, "Assign"),
        (3, "Handouts"),
        (4, "Resources"),
        (9, "Other"),
    )

    ELEMENT_CHOICES = (
        (0, "Activity"),
        (1, "Agenda"),
        (2, "Assign"),
        (3, "Big story"),
        (4, "Break"),
        (5, "Exercise"),
        (6, "Highlights"),
        (7, "Prompt"),
        (8, "Readings"),
        (9, "Share 1"),
        (10, "Wheel"),
        (11, "Tips"),
        (12, "Template"),
        (13, "Transcript"),
        (14, "Video"),
        (15, "Sample"),
        (16, "Share 2"),
        (99, "Other"),
    )

    courseweek    = models.ForeignKey(JOSCourseWeek, blank=True, null=True)
    part_no       = models.IntegerField(default=9, choices=PART_CHOICES)
    segment_no    = models.IntegerField(default=9, choices=SEGMENT_CHOICES)
    element_no    = models.IntegerField(default=99, choices=ELEMENT_CHOICES)
    element_order = models.IntegerField(default=0)

    publish = models.BooleanField(default=False)

    pdf_handout = models.FileField(upload_to=upload_to("joscourses-handouts.pdf_handout", "joscourses"),
                          max_length=255, null=True, blank=True)

    def __unicode__(self):
        return 'Handout #'+str(self.id)
