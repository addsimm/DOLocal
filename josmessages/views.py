from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.timezone import activate
from django.contrib.auth.models import User

from josmessages.models import Message, JOSMessageThread
from josmessages.forms import JOSComposeForm, JOSReplyForm

from josmembers.models import JOSTeam

if "notification" in settings.INSTALLED_APPS and getattr(settings, "JOSMESSAGES_NOTIFY", True):
    from notification import models as notification
else:
    notification = None


@login_required
def inbox(request, template_name="josmessages/inbox.html"):
    """
    Displays a list of received messages for the current user.
    """
    activate('America/Los_Angeles')

    pot_message_list = Message.objects.filter(recipient=request.user, recipient_deleted_at__isnull=True).order_by('-sent_at')

    message_list = pot_message_list.order_by('message_thread__subject').distinct('message_thread__subject')

    return render_to_response(template_name,
                              {"message_list": message_list},
                              context_instance=RequestContext(request))


@login_required
def outbox(request, template_name="josmessages/outbox.html"):
    """
    Displays a list of sent messages by the current user.
    """
    activate('America/Los_Angeles')
    message_list = Message.objects.outbox_for(request.user)
    return render_to_response(template_name, {
        "message_list": message_list,
    }, context_instance=RequestContext(request))


@login_required
def trash(request, template_name="josmessages/trash.html"):
    """
    Displays a list of deleted messages.
    Hint: A Cron-Job could periodically clean up old messages
    """
    activate('America/Los_Angeles')
    message_list = JOSMessageThread.objects.trash_for(request.user)
    return render_to_response(template_name, {
        "message_list": message_list,
    }, context_instance=RequestContext(request))


@login_required
def delete(request, message_thread_id=0):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete
    A cron-job should prune the database and remove old messages
    As a side effect, this makes it easy to implement a trash with undelete.

    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    activate('America/Los_Angeles')
    user = request.user
    now = timezone.now()
    try:
        message_thread = get_object_or_404(JOSMessageThread, id=message_thread_id)
    except:
        raise Http404

    message_list = Message.objects.filter(message_thread=message_thread)

    for message in message_list:
        message.read_at = now
        message.recipient_deleted_at = now
        message.save()

    messages.info(request, "Message successfully deleted.")
    return redirect('http://www.joinourstory.com/messages/inbox/')


### JOS Messaging
@login_required
def jos_message_compose(request, id=None,
                        form_class=JOSComposeForm,
                        template_name="josmessages/compose.html",
                        recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a "+"
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfully submission
    """

    recip_ids =[]
    recipients = []

    team_name = request.GET.get('team', None)

    if team_name != None:
        team = get_object_or_404(JOSTeam, name=team_name)
        team_member_ids = team.member_id_list()
        recip_ids = team_member_ids
        if len(team_member_ids) > 0:
            for member_id in team_member_ids:
                recipient = User.objects.get(id=member_id)
                recipients.append(recipient)
    else:
        recipient = User.objects.get(id=id)
        recipients.append(recipient)
        recip_ids.append(id)

    form = form_class()

    if request.method == "POST":
        if request.method == "POST":
            form = JOSReplyForm(request.POST)
            if form.is_valid():
                body = request.POST["body"]
                subject = request.POST["subject"]

                mt = JOSMessageThread.objects.create(subject=subject)
                mt.save()

                for recip_id in recip_ids:
                    try:
                        recipient = get_object_or_404(User, pk=recip_id)
                    except:
                        continue
                    msg = Message.objects.create(
                            body=body,
                            message_thread=mt,
                            sender=request.user,
                            recipient=recipient,
                            sent_at=timezone.now()
                    )

                    msg.save()

                messages.info(request, "Message successfully sent.")

                if notification:
                    # notification.send([sender], "messages_sent", {'message': msg,})
                    # notification.send([recipients], "messages_received", {'message': msg,})
                    # return msg
                    pass

                return HttpResponseRedirect(reverse("josmessages:messages_inbox"))

    return render_to_response(template_name, {
        "form": form,
        "recipients": recipients
    }, context_instance=RequestContext(request))


@login_required
def view(request, message_thread_id = 0, template_name="josmessages/view.html"):
    """
    Shows a single message thread with reply option.
    """
    activate('America/Los_Angeles')
    message_thread = get_object_or_404(JOSMessageThread, id=message_thread_id)
    messages = message_thread.messages.filter(recipient=request.user).order_by("sent_at")
    for message in messages:
        if not message.read_at:
            message.read_at = timezone.now()
            message.save()

    recipients = message_thread.recipients
    form = JOSReplyForm({"message_thread_id": message_thread.id})

    if request.method == "POST":
        form = JOSReplyForm(request.POST)
        if form.is_valid():
            for message in messages:
                if not message.replied_at:
                    message.replied_at = timezone.now()

            mt_id = request.POST["message_thread_id"]
            body = request.POST["body"]
            mt = get_object_or_404(JOSMessageThread, pk=mt_id)

            for recipient in recipients:
                message = Message.objects.create(
                    message_thread=mt,
                    body=body,
                    sender=request.user,
                    recipient =recipient,
                    sent_at=timezone.now()
                )
                message.save()

            messages.info(request, "Message successfully sent.")
            return HttpResponseRedirect(reverse("josmessages:messages_inbox"))

    context = {"form": form,
               "subject": message_thread.subject,
               "recipients": recipients,
               "messages": messages,
               "message_thread_id": message_thread.id}

    return render_to_response(template_name, context, context_instance=RequestContext(request))


    # @login_required
    # def undelete(request, message_id, success_url=None):
    #     """
    #     Recovers a message from trash. This is achieved by removing the
    #     ``(sender|recipient)_deleted_at`` from the model.
    #     """
    #     user = request.user
    #     message = get_object_or_404(Message, id=message_id)
    #     undeleted = False
    #     if success_url is None:
    #         success_url = reverse("josmessages:messages_inbox")
    #     if "next" in request.GET:
    #         success_url = request.GET["next"]
    #     if message.sender == user:
    #         message.sender_deleted_at = None
    #         undeleted = True
    #     if message.recipient == user:
    #         message.recipient_deleted_at = None
    #         undeleted = True
    #     if undeleted:
    #         message.save()
    #         messages.info(request, _(u"Message successfully recovered."))
    #         if notification:
    #             notification.send([user], "messages_recovered", {"message": message,})
    #         return HttpResponseRedirect(success_url)
    #     raise Http404