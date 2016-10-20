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


class JOSReplyForm(forms.Form):
    """
    Validates body
    """
    message_thread_id = forms.IntegerField(label=_(u"message_thread"))
    body = forms.CharField(label=_(u"Body"),
                           widget=forms.Textarea(attrs={'rows': '15', 'cols': '65'}))
    def __init__(self, *args, **kwargs):
        super(JOSReplyForm, self).__init__(*args, **kwargs)

        self.fields['body'].required = True
