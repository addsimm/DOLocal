from django.contrib.auth.models import User
from django.db import models

from mezzanine.core.models import TimeStamped

from ckeditor.fields import RichTextField

# Create your models here.


class CKRichTextHolder(TimeStamped, models.Model):
    class Meta:
        verbose_name = 'CK Rich Text Holder'

    author = models.ForeignKey(User)
    title = models.CharField(max_length=150, default="untitled")
    field_to_edit = models.CharField(max_length=150, default="nofield")
    content = RichTextField()

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
    title = models.CharField(max_length=150, default="untitled")
    content = RichTextField()
    publish = models.BooleanField(default=False)

    def get_jos_name(author):
        first_name = author.get_short_name()[:9]
        last_initial = author.user.last_name[:1].upper()
        jos_name = first_name + " " + last_initial + "."
        return jos_name