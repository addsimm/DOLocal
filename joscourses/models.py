from django.db import models

from django.contrib.auth.models import User

from mezzanine.core.models import TimeStamped
from mezzanine.utils.models import upload_to

from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager

from josmessages.models import JOSMessageThread

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
        (0, "Activity 1"),
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
        (17, "Activity 2"),
        (99, "Other"),
    )

    courseweek    = models.ForeignKey(JOSCourseWeek, blank=True, null=True)
    part_no       = models.IntegerField(default=9, choices=PART_CHOICES)
    segment_no    = models.IntegerField(default=9, choices=SEGMENT_CHOICES)
    element_no    = models.IntegerField(default=99, choices=ELEMENT_CHOICES)
    element_order = models.IntegerField(default=0)

    publish = models.BooleanField(default=False)

    pdf_handout = models.FileField(upload_to=upload_to("joscourses-handouts.pdf_handout", "joscourses"), max_length=255, null=True, blank=True)

    def __unicode__(self):
        return 'Handout #'+str(self.id)


class JOSStory(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'

    message_thread = models.ForeignKey(JOSMessageThread, null=True)
    author = models.ForeignKey(User)
    title = models.TextField(default="Untitled")
    content = models.TextField(default="Coming soon")
    publish_permission = models.IntegerField(default=1)
    tags = TaggableManager()

    def get_jos_name(author):
        first_name = author.get_short_name()[:9]
        last_initial = author.user.last_name[:1].upper()
        jos_name = first_name + " " + last_initial + "."
        return jos_name


class JOSStorywheel(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Storywheel'

    author = models.ForeignKey(User, blank=True, null=True)
    title = models.TextField(default="Untitled", blank=True, null=True)
    publish_permission = models.IntegerField(default=1)
    tags = TaggableManager()


class JOSPlotTemplate(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'Plot Template'
        verbose_name_plural = 'Plot Templates'

    storywheel = models.ForeignKey(JOSStorywheel, blank=True, null=True)
    publish_permission = models.IntegerField(default=1)
    incite = models.TextField(default="-- insert inciting incident --", blank=True, null=True)
    rising = models.TextField(default="-- insert rising action --", blank=True, null=True)
    climax = models.TextField(default="-- insert climax --", blank=True, null=True)
    falling = models.TextField(default="-- insert falling action --", blank=True, null=True)
    resolve = models.TextField(default="-- insert resolution --", blank=True, null=True)



