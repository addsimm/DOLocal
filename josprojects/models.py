from django.contrib.auth.models import User
from django.db import models

from mezzanine.core.models import TimeStamped

# Create your models here.

class CKRichTextHolder(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS CKE Holder'

    author = models.ForeignKey(User)
    parent_class = models.CharField(max_length=150, default="no_object")
    parent_id = models.IntegerField(default=0)
    field_edited = models.CharField(max_length=150, default="no_field")
    content = models.TextField()

    def get_jos_name(author):
        first_name = author.get_short_name()[:9]
        last_initial = author.user.last_name[:1].upper()
        jos_name = first_name + " " + last_initial + "."
        return jos_name


class JOSStory(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'JOS Story'
        verbose_name_plural = 'JOS Stories'

    author = models.ForeignKey(User)
    title = models.TextField(default="untitled")
    content = models.TextField()
    publish = models.BooleanField(default=False)

    def get_jos_name(author):
        first_name = author.get_short_name()[:9]
        last_initial = author.user.last_name[:1].upper()
        jos_name = first_name + " " + last_initial + "."
        return jos_name