import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.shortcuts import get_object_or_404

from josmessages.models import Message, JOSMessageThread
from josmessages.fields import CommaSeparatedUserField
from josmessages.utils import get_user_model

User = get_user_model()

if "notification" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    from notification import models as notification
else:
    notification = None


class JOSComposeForm(forms.Form):
    """
    A jos compose message form that hides sender and fixes the recipients.
    """
    subject = forms.CharField(label=_(u"Subject"), max_length=120)
    body = forms.CharField(label=_(u"Body"), widget=forms.Textarea(attrs={'rows': '15', 'cols': '65'}))

    def __init__(self, *args, **kwargs):
        super(JOSComposeForm, self).__init__(*args, **kwargs)
        self.fields['subject'].required = True
        self.fields['body'].required = True
        self.fields['body'].label = "Message"

    def save(self, sender=None, recip_ids=None):
        body = self.cleaned_data['body']
        subject = self.cleaned_data['subject']

        mt = JOSMessageThread.objects.create(
                subject=subject,
                message_count=1)

        for recip_id in recip_ids:
            try:
                recipient = get_object_or_404(User, pk=recip_id)
            except:
                continue
            msg = Message.objects.create(
                body=body,
                message_thread=mt,
                sender=sender,
                recipient=recipient,
                sent_at=timezone.now()
            )

            mt.last_message_id = msg.id
            ##### mt.last_recipient = recipient,
            msg.save()

        mt.save()
        if notification:
            # notification.send([sender], "messages_sent", {'message': msg,})
            # notification.send([recipients], "messages_received", {'message': msg,})
            # return msg
            pass

class JOSReplyForm(forms.Form):
    """
    Validates body
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    message_thread_id = forms.IntegerField(label=_(u"message_thread"))
    body = forms.CharField(label=_(u"Body"),
                           widget=forms.Textarea(attrs={'rows': '15', 'cols': '65'}))
    def __init__(self, *args, **kwargs):
        super(JOSReplyForm, self).__init__(*args, **kwargs)

        self.fields['body'].required = True
