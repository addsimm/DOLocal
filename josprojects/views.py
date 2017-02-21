from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template.response import TemplateResponse
from django.utils.timezone import activate
from django.views.decorators.csrf import csrf_exempt

from joscourses.models import JOSCourseWeek
from josmembers.models import  JOSProfile, JOSUserCreatedNote

from josmembers.models import JOSTeam
from joscourses.models import JOSStory
from josprojects.models import JOSHelpItem

# Create your views here.

User = get_user_model()

@login_required
def personaldesk(request, pk, template="josprojects/personal_desk.html", extra_context=None):
    user = get_object_or_404(User, pk=pk)

    activate('America/Los_Angeles')

    current_profile = get_object_or_404(JOSProfile, user=user)
    weeks = JOSCourseWeek.objects.filter(publish=True).order_by('week_no') # retrieves all weeks available

    context = {"profile": current_profile, "weeks": weeks}
    context.update(extra_context or {})

    return render(request, template, context)


@login_required
def mystory_list(request, template="josprojects/my_story_list.html", extra_context=None):
    activate('America/Los_Angeles')
    stories = JOSStory.objects.filter(author=request.user).order_by('-updated')

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def story_gallery(request, template="josprojects/story_gallery.html", extra_context=None):
    activate('America/Los_Angeles')

    team_member_id_list = []
    stories = []
    team_name = 'xxx'

    team_no = int(request.GET.get('team', 0))
    if team_no == 0:
        stories = JOSStory.objects.filter(publish_permission=3).order_by('-updated')

    else:
        team = get_object_or_404(JOSTeam, pk=team_no)
        team_member_id_list = team.member_id_list()
        team_name = team.name

        if len(team_member_id_list) > 0:
            for id in team_member_id_list:
                user = get_object_or_404(User, pk=id)
                user_stories = JOSStory.objects.filter(author=user, publish_permission__gt=1)
                for story in user_stories:
                    stories.append(story)

    context = {'stories': stories,
               'team_name': team_name}

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def community_room(request, incognito=False, jos_id=0, template="josprojects/chat_room.html"):
    JOSKey = 'e18f2a1f-f608-44ae-8fc9-e2a42bb0278e'
    try:
        user = get_object_or_404(User, pk=jos_id)
        josname = user.JOSProfile.friendly_jos_name()
    except:
        josname = "???"

    #### to login user:
    # user.backend = 'django.contrib.auth.backends.ModelBackend'
    # auth_login(request, user)
    context = {
        'JOSKey': JOSKey,
        'JOSId': jos_id,
        'JOSName': josname,
        'incognito': incognito
    }

    return TemplateResponse(request, template, context)


@login_required
def workshop_connect(request, template="josprojects/workshop_connect.html"):
    context = {}
    return TemplateResponse(request, template, context)


def ajax_help_search(request):
    help_search_text = ""  # Assume no search
    context = {}

    if (request.method == "GET"):
        """
        The search form has been submitted. Get the search text - must be GET.
        """
        help_search_text = request.GET.get("help_search_text", "").strip().lower()

        if help_search_text.isdigit():
            id = int(help_search_text)
            try:
                help_item = get_object_or_404(JOSHelpItem, pk=id)
                help_item_content = help_item.title + ':<br>' + help_item.content

            except:
                help_item_content = ' '

            return HttpResponse(help_item_content)

        else:
            help_items = []

            if (help_search_text != ""):
                help_items = JOSHelpItem.objects.filter(title__icontains=help_search_text)

            context = {
                'help_search_text': help_search_text,
                'help_items':       help_items
            }

            return render_to_response("josprojects/ajax_help_search_results.txt", context)

@login_required
@csrf_exempt
def ajax_session_update(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('not ok')

    user_profile = get_object_or_404(JOSProfile, user=request.user)

    new_note_content = request.POST.get('new_content', 'missing')

    if new_note_content != 'missing':
        user_created_note = get_object_or_404(JOSUserCreatedNote, profile=user_profile)

        user_created_note.note_text = new_note_content
        user_created_note.save()
        info(request, "Notes updated!")

    # Update help status in session data
    help_position = request.POST.get("help_position", 'missing')
    active_tab = request.POST.get("active_tab", 'missing')
    help_item_no = request.POST.get("help_item_no", 'missing')
    editor_status = request.POST.get("editor_status", 'missing')
    wheel_position = request.POST.get("wheel_position", 'missing')

    if active_tab != 'missing':
        request.session["active_tab"] = active_tab

    if help_position != 'missing':
        request.session["help_position"] = help_position

    if help_item_no != 'missing':
        request.session["help_item_no"] = help_item_no

    if editor_status != 'missing':
        request.session["editor_status"] = editor_status

    if wheel_position != 'missing':
        request.session["wheel_position"] = wheel_position

    return HttpResponse('ok')


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
