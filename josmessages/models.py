from django.conf import settings
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

from mezzanine.core.models import TimeStamped

class MessageManager(models.Manager):
    def outbox_for(self, user):
        """
        Returns all messages that were sent by the given user and are not
        marked as deleted.
        """
        return self.filter(
                sender=user
        )

@python_2_unicode_compatible
class JOSMessageThread(TimeStamped, models.Model):
    # A holder for messages in a thread
    ### objects = JOSMessageThreadManager()

    class Meta:
        verbose_name = "Thread"

    subject = models.CharField(default='missing', max_length=255, null=True, blank=True)
    first_recipient_id = models.CharField(default='missing', max_length=255, null=True, blank=True)

    @property
    def messages(self):
        return Message.objects.filter(message_thread=self)

    @property
    def messages_distinct_user_ids(self):
        user_ids = []
        user_ids.append(int(self.first_recipient_id))
        recipient_id_dicts = Message.objects.filter(message_thread=self).values('recipient')
        sender_id_dicts = Message.objects.filter(message_thread=self).values('sender')
        for dict in recipient_id_dicts:
            user_ids.append(dict.values()[0])
        for dict in sender_id_dicts:
            user_ids.append(dict.values()[0])
        return list(set(user_ids))

    def __str__(self):
        return self.subject


@python_2_unicode_compatible
class Message(models.Model):
    #A message / comment

    objects = MessageManager() # handles outbox

    message_thread = models.ForeignKey("JOSMessageThread", related_name="comments", null=True)
    body = models.TextField(verbose_name="Body", default='missing')

    sender = models.ForeignKey(User, related_name='sent_messages', verbose_name="Sender")

    sent_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    recipient = models.ForeignKey(User, related_name='received_messages', null=True, blank=True, verbose_name= "Recipient")

    read_at = models.DateTimeField(verbose_name="read at", null=True, blank=True)
    replied_at = models.DateTimeField(verbose_name="replied at", null=True, blank=True)
    recipient_deleted_at = models.DateTimeField(verbose_name="Recipient deleted at", null=True, blank=True)

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

    def save(self, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)

    @property
    def subject(self):
        return self.message_thread.subject

    def __str__(self):
        return self.body

    class Meta:
        ordering = ["-sent_at"]
        verbose_name = "Message"


def inbox_count_for(user):
    """
    returns the number of unread messages for the user
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True).count()

# fallback for email notification if django-notification could not be found
if "notification" not in settings.INSTALLED_APPS and getattr(settings, "JOSMESSAGES_NOTIFY", True):
    from josmessages.utils import new_message_email
    signals.post_save.connect(new_message_email, sender=Message)


# class JOSMessageThreadManager(models.Manager):
#
#     def trash_for(self, user):
#         """
#         Returns all messages that were either received or sent by the given
#         user and are marked as deleted.
#         """
#         return self.filter(
#             last_recipient=user,
#             is_deleted=True,
#         )
