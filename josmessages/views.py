from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.timezone import activate

from josmessages.models import Message, JOSMessageThread
from josmessages.forms import JOSComposeForm, JOSReplyForm
from josmessages.utils import get_user_model

User = get_user_model()

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
    thread_list = JOSMessageThread.objects.inbox_for(request.user)
    message_list = []
    for thread in thread_list:
        message_id = thread.last_message_id
        message = get_object_or_404(Message, pk=message_id)
        message_list.append(message)

    message_list.sort(key=lambda x: x.sent_at, reverse=True)
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
    Hint: A Cron-Job could periodicly clean up old messages
    """
    activate('America/Los_Angeles')
    message_list = JOSMessageThread.objects.trash_for(request.user)
    return render_to_response(template_name, {
        "message_list": message_list,
    }, context_instance=RequestContext(request))


@login_required
def delete(request, message_thread_id=0, success_url=None):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete a message
    before it"s save to remove it completely.
    A cron-job should prune the database and remove old messages which are
    deleted by both users.
    As a side effect, this makes it easy to implement a trash with undelete.

    You can pass ?next=/foo/bar/ via the url to redirect the user to a different
    page (e.g. `/foo/bar/`) than ``success_url`` after deletion of the message.
    """
    user = request.user
    now = timezone.now()
    try:
        message_thread = get_object_or_404(JOSMessageThread, id=message_thread_id)
    except:
        raise Http404
    try:
        message = get_object_or_404(Message, id=message_thread.last_message_id)
    except:
        raise Http404

    message_thread.is_deleted = True

    if message.sender == user:
        message.sender_deleted_at = now

    if message.recipient == user:
        message.recipient_deleted_at = now

    message_thread.save()
    message.save()
    messages.info(request, _(u"Message successfully deleted."))
    return redirect('http://www.joinourstory.com/messages/inbox/')


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

### JOS Messaging
@login_required
def jos_message_compose(request, id=None, form_class=JOSComposeForm,
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
        ``success_url``: where to redirect after successfull submission
    """

    form = form_class()
    recipient = User.objects.get(id=id)
    if request.method == "POST":
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            mt = JOSMessageThread.objects.create(
                subject = request.POST["subject"],
                last_recipient = recipient,
                message_count = 1)

            msg = form.save(sender=request.user, recipient=recipient, message_thread=mt)
            mt.last_message_id = msg.id
            mt.save()
            messages.info(request, _(u"Message successfully sent."))

            return HttpResponseRedirect(reverse("josmessages:messages_inbox"))

    return render_to_response(template_name, {
        "form": form,
        "recipient": recipient
    }, context_instance=RequestContext(request))

@login_required
def view(request, message_thread_id = 0, template_name="josmessages/view.html"):
    """
    Shows a single message thread with reply option.
    """
    activate('America/Los_Angeles')
    message_thread = get_object_or_404(JOSMessageThread, id=message_thread_id)
    last_message = get_object_or_404(Message, id=message_thread.last_message_id)
    last_message.read_at = timezone.now()
    last_message.is_last = False
    if last_message.sender != request.user:
        recipient = last_message.sender
    else:
        recipient = last_message.recipient
    last_message.save()

    form = JOSReplyForm({"message_thread_id": message_thread.id})
    bodies = Message.objects.filter(message_thread=message_thread).order_by("sent_at")

    if request.method == "POST":
        form = JOSReplyForm(request.POST)
        if form.is_valid():
            last_message.replied_at = timezone.now()
            last_message.save()
            mtid = request.POST["message_thread_id"]
            body = request.POST["body"]
            mt = get_object_or_404(JOSMessageThread, pk=mtid)

            message = Message.objects.create(
                message_thread=mt,
                body=body,
                sender=request.user,
                recipient =recipient,
                sent_at=timezone.now(),
                is_last=True)
            message.save()

            mt_count = mt.message_count
            mt.message_count = mt_count + 1
            mt.last_message_id = message.id
            mt.last_recipient = recipient
            mt.save()

            messages.info(request, _(u"Message successfully sent."))
            return HttpResponseRedirect(reverse("josmessages:messages_inbox"))

    context = {"form": form,
               "subject": message_thread.subject,
               "recipient": recipient,
               "bodies": bodies,
               "message_thread_id": message_thread.id}

    return render_to_response(template_name, context, context_instance=RequestContext(request))
