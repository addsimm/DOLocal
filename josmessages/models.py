from django.conf import settings
from django.db import models
from django.db.models import signals, F
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import TimeStamped

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class MessageManager(models.Manager):

    def inbox_for(self, user):
        """
        Returns all messages that were received by the given user and are not
        marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=True,
        )

    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
            sender=user,
            sender_deleted_at__isnull=True,
        )

    def trash_for(self, user):
        """
        Returns all messages that were either received or sent by the given
        user and are marked as deleted.
        """
        return self.filter(
            recipient=user,
            recipient_deleted_at__isnull=False,
        ) | self.filter(
            sender=user,
            sender_deleted_at__isnull=False,
        )


@python_2_unicode_compatible
class JOSMessageThread(TimeStamped, models.Model):
    """
    A holder for messages in a thread
    """
    title = models.CharField(_("title"), max_length=255, blank=True)
    message_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title + '_' + str(self.id)

    class Meta:
        ordering = ['-updated']
        verbose_name = _("Message Thread")
        verbose_name_plural = _("Message Threads")


@python_2_unicode_compatible
class Message(models.Model):
    """
    A message / comment
    """

    objects = MessageManager()

    body = models.TextField(_("Body"))
    parent_msg = models.ForeignKey('self', related_name='next_messages', null=True, blank=True, verbose_name=_("Parent message"))
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages', null=True, blank=True, verbose_name=_("Recipient"))
    recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), null=True, blank=True)
    replied_at = models.DateTimeField(_("replied at"), null=True, blank=True)
    sender = models.ForeignKey(AUTH_USER_MODEL, related_name='sent_messages', verbose_name=_("Sender"))
    sender_deleted_at = models.DateTimeField(_("Sender deleted at"), null=True, blank=True)
    sent_at = models.DateTimeField(_("sent at"), null=True, blank=True)
    subject = models.CharField(_("Subject"), max_length=120, blank=True, null=True)

    # NEW

    is_removed = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(_("likes count"), default=0)
    josmessagethread = models.ForeignKey('JOSMessageThread', related_name='comments', null=True)

    @property
    def like(self):
        # *likes* is dynamically created by manager.with_likes()
        try:
            assert len(self.likes) <= 1, "Panic, too many likes"
            return self.likes[0]
        except (AttributeError, IndexError):
            return


    def increase_likes_count(self):
        Message.objects \
            .filter(pk=self.pk) \
            .update(likes_count=F('likes_count') + 1)


    @classmethod
    def get_last_for_topic(cls, topic_id):
        return (cls.objects
                .filter(topic_id=topic_id)
                .order_by('pk')
                .last())

    # OLD

    def new(self):
        """returns whether the recipient has read the message or not"""
        if self.read_at is not None:
            return False
        return True

    def replied(self):
        """returns whether the recipient has written a reply to this message"""
        if self.replied_at is not None:
            return True
        return False

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return ('josmessages:messages_detail', [self.id])
    get_absolute_url = models.permalink(get_absolute_url)

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


def inbox_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()

# fallback for email notification if django-notification could not be found
if "notification" not in settings.INSTALLED_APPS and getattr(settings, 'JOSMESSAGES_NOTIFY', True):
    from josmessages.utils import new_message_email
    signals.post_save.connect(new_message_email, sender=Message)


