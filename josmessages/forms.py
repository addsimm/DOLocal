import datetime

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

if "notification" in settings.INSTALLED_APPS and getattr(settings, 'DJANGO_MESSAGES_NOTIFY', True):
    from notification import models as notification
else:
    notification = None

from josmessages.models import Message
from josmessages.fields import CommaSeparatedUserField

# class ComposeForm(forms.Form):
#     """
#     A simple default form for private messages.
#     """
#     recipient = CommaSeparatedUserField(label=_(u"Recipient"))
#     subject = forms.CharField(label=_(u"Subject"), max_length=120)
#     body = forms.CharField(label=_(u"Body"),
#         widget=forms.Textarea(attrs={'rows': '12', 'cols':'55'}))
#
#
#     def __init__(self, *args, **kwargs):
#         recipient_filter = kwargs.pop('recipient_filter', None)
#         super(ComposeForm, self).__init__(*args, **kwargs)
#         if recipient_filter is not None:
#             self.fields['recipient']._recipient_filter = recipient_filter
#
#
#     def save(self, sender, parent_msg=None):
#         recipients = self.cleaned_data['recipient']
#         subject = self.cleaned_data['subject']
#         body = self.cleaned_data['body']
#         message_list = []
#         for r in recipients:
#             msg = Message(
#                 sender = sender,
#                 recipient = r,
#                 subject = subject,
#                 body = body,
#             )
#             if parent_msg is not None:
#                 msg.parent_msg = parent_msg
#                 parent_msg.replied_at = timezone.now()
#                 parent_msg.save()
#             msg.save()
#             message_list.append(msg)
#             if notification:
#                 if parent_msg is not None:
#                     notification.send([sender], "messages_replied", {'message': msg,
#                                                                      'message_sender': sender})
#                     notification.send([r], "messages_reply_received", {'message': msg,
#                                                                        'message_parent_msg': subject,
#                                                                        'message_recipient': recipients})
#                 else:
#                     notification.send([sender], "messages_sent", {'message': msg,
#                                                                   'message_sender': sender})
#                     notification.send([r], "messages_received", {'message': msg,
#                                                                  'message_parent_msg': subject,
#                                                                  'message_recipient': recipients})

class JOSComposeForm(forms.Form):
    """
    A jos message form that hides sender.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=120)
    body = forms.CharField(label=_(u"Body"),
                           widget=forms.Textarea(attrs={'rows': '15', 'cols': '65'}))

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(JOSComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter

        self.fields['recipient'].requred = False
        self.fields['subject'].required = True
        self.fields['body'].required = True
        self.fields['body'].label = "Message"

    def save(self, sender=None, recipient=None, message_thread=None):
        body = self.cleaned_data['body']
        msg = Message.objects.create(
            body=body,
            message_thread=message_thread,
            sender=sender,
            recipient=recipient,
            sent_at=timezone.now()
        )
        msg.save()

        if notification:
            notification.send([sender], "messages_sent", {'message': msg,})
            notification.send([recipient], "messages_received", {'message': msg,})
        return msg


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
