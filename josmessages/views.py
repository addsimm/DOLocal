

from django.contrib import messages as response_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import info
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.timezone import activate

from mezzanine.conf import settings

from friendship.exceptions import AlreadyExistsError
from friendship.models import Follow

from josmessages.forms import JOSComposeForm
from josmessages.models import Message, JOSMessageThread

from josmembers.models import JOSTeam

if "notification" in settings.INSTALLED_APPS and getattr(settings, "JOSMESSAGES_NOTIFY", True):
    from notification import models as notification
else:
    notification = None


@login_required
def delete(request, message_thread_id=0):
    """
    Marks a message as deleted by sender or recipient. The message is not
    really removed from the database, because two users must delete
    A cron-job should prune the database and remove aaold messages
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

    response_messages.info(request, "Message successfully deleted.")
    return redirect('http://www.joinourstory.com/messages/inbox/')


@login_required
def message_box(request, template_name="josmessages/mailbase.html"):
    activate('America/Los_Angeles')

    # Messages
    distinct_inbox_list = list(Message.objects
                .filter(recipient=request.user, recipient_deleted_at__isnull=True)
                .distinct('message_thread__subject')
                .order_by('message_thread__subject'))

    inbox_list = sorted(distinct_inbox_list, key=lambda message: -message.id)

    # List of who user is following
    following = Follow.objects.following(request.user)

    # List of user's circles
    teams = request.user.JOSProfile.teams.all()
    teams_list = []
    for team in teams:
        team_dict = {}
        team_dict.update({'name': team.name})
        team_users = []
        for team_member in team.member_id_list():
            team_users.append(User.objects.get(pk=team_member))

        team_dict.update({'users': team_users})
        teams_list.append(team_dict)

    # sent_list = Message.objects.outbox_for(request.user)[0:4]

    context = {
        "inbox_list": inbox_list,
        "teams_list": teams_list,
        "following":  following
        # "sent_list":  sent_list
    }

    return render(request, template_name, context)


### JOS Messaging
@login_required
def jos_message_compose(request, id=None, template_name="josmessages/compose.html", recipient_filter=None):

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

    form = JOSComposeForm()

    if request.method == "POST":
        if request.method == "POST":
            form = JOSComposeForm(request.POST)
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
                            recipient=recipient
                    )

                    msg.save()

                response_messages.info(request, "Message successfully sent.")

                if notification:
                    # notification.send([sender], "messages_sent", {'message': msg,})
                    # notification.send([recipients], "messages_received", {'message': msg,})
                    # return msg
                    pass

                return HttpResponseRedirect(reverse("josmessages:messages_inbox"))

    return render(request, template_name, {
        "form": form,
        "recipients": recipients,
        "recip_ids": recip_ids
    })


def ajax_message_info(request):
    if not request.is_ajax():
        return HttpResponse('Not ajax')

    # favorites
    if request.method == "GET":

        ### favorite_user
        # favorite_user_id = int(request.GET.get('favorite_user_id', '0'))
        # if favorite_user_id > 0:
        #     try:
        #         other_user = get_object_or_404(User, pk=favorite_user_id)
        #         Follow.objects.add_follower(request.user, other_user)
        #         info(request, other_user.JOSProfile.friendly_jos_name() + " is now a favorite!")
        #     except ValidationError:
        #         info(request, "You cannot favorite yourself ...")
        #     except AlreadyExistsError:
        #         info(request, other_user.JOSProfile.friendly_jos_name() + " is already a favorite!")
        #
        #     return HttpResponse('ok')

        ### un favor_user
        # remove_user_id = int(request.GET.get('remove_user_id', '0'))
        # if remove_user_id > 0:
        #     try:
        #         remove_user = User.objects.get(id=remove_user_id)
        #         return_variable = Follow.objects.remove_follower(request.user, remove_user)
        #         if return_variable:
        #             info(request, remove_user.JOSProfile.friendly_jos_name() + " is no longer a favorite.")
        #         else:
        #             info(request, "Sorry, can't remove favorite - please contact us.")
        #     except:
        #         return HttpResponse('remove favorite fail: ' + str(remove_user_id))
        #
        #     return HttpResponse('ok')

        recip_ids = []
        recipients = []

        # compose_message_to = request.GET.get('compose_message_to', '0')
        # message_to_id = request.GET.get('message_to_id', '0')
        # if compose_message_to != '0':
        #     new_message_thread = JOSMessageThread.objects.create(
        #             subject = 'missing',
        #             first_recipient_id = message_to_id)
        #
        #     if compose_message_to == 'member':
        #         recip = get_object_or_404(User, pk=int(message_to_id))
        #         recipients.append(recip)
        #
        #     context = {
        #         "message_thread": new_message_thread,
        #         "recipients":     recipients,
        #     }
        #
        #     return render(request, "josmessages/view.html", context)

        # team_name = request.GET.get('team', None)
        # if team_name != None:
        #     team = get_object_or_404(JOSTeam, name=team_name)
        #     team_member_ids = team.member_id_list()
        #     recip_ids = team_member_ids
        #     if len(team_member_ids) > 0:
        #         for member_id in team_member_ids:
        #             recipient = User.objects.get(id=member_id)
        #             recipients.append(recipient)
        # else:
        #     recipient = User.objects.get(id=id)
        #     recipients.append(recipient)
        #     recip_ids.append(id)

    message_thread_id = "0"

    if request.method == "GET":
        message_thread_id = int(request.GET.get("message_thread_id", "0"))
    elif request.method == "POST":
        message_thread_id = int(request.POST.get("message_thread_id", "0"))

    if message_thread_id > 0:
        msg_thread = get_object_or_404(JOSMessageThread, id=message_thread_id)
        all_thread_msgs = msg_thread.messages
    else:
        return HttpResponse('Thread not found; message_thread_id: ' + str(message_thread_id))

    unique_recip_ids = msg_thread.messages_distinct_user_ids
    recipients = []
    for usr_id in unique_recip_ids:
        recip = get_object_or_404(User, pk=usr_id)
        recipients.append(recip)

    msgs = all_thread_msgs.filter(Q(recipient=request.user) | Q(sender=request.user))
    unique_msgs = list(msgs.distinct('body').order_by('body'))

    sort_msgs = sorted(unique_msgs, key=lambda message: -message.id)

    if request.method == "GET":
        for msg in msgs:
            if not msg.read_at:
                msg.read_at = timezone.now()
                msg.save()

        context = {
            "message_thread": msg_thread,
            "recipients": recipients,
            "emails": sort_msgs
        }

        return render(request, "josmessages/view.html", context)

    # if request.method == 'POST':
    #     reply_content = request.POST.get('reply_content', 'missing')
    #     msgs_user_ids = msg_thread.messages_distinct_user_ids
    #
    #     if len(msgs) > 0:
    #         for msg in msgs:
    #             if not msg.replied_at:
    #                 msg.replied_at = timezone.now()
    #                 msg.save()
    #
    #     for xid in msgs_user_ids:
    #         if xid != request.user.id:
    #             recip = get_object_or_404(User, pk=xid)
    #
    #             send_message = Message.objects.create(
    #                     body=reply_content,
    #                     message_thread=msg_thread,
    #                     recipient=recip,
    #                     sender=request.user
    #             )
    #             send_message.save()
    #             info(request, "Message successfully sent!")
    #
    #     return HttpResponse("Reply sent; message_thread_id: " + str(message_thread_id))

    return HttpResponse('ajax_message_info fell through')




































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
    #         response_messages(request, _(u"Message successfully recovered."))
    #         if notification:
    #             notification.send([user], "messages_recovered", {"message": message,})
    #         return HttpResponseRedirect(success_url)
    #     raise Http404


    # @login_required
    # def trash(request, template_name="josmessages/trash.html"):
    #     """
    #     Displays a list of deleted messages.
    #     Hint: A Cron-Job could periodically clean up aaold messages
    #     """
    #     activate('America/Los_Angeles')
    #     message_list = JOSMessageThread.objects.trash_for(request.user)
    #     return render(request, template_name, {"message_list": message_list})