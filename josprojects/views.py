from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import activate
from django.views.decorators.csrf import csrf_exempt

from joscourses.models import JOSCourseWeek
from josmembers.models import JOSProfile
from josmessages.models import Message, JOSMessageThread

from josmembers.models import JOSTeam
from .models import CKRichTextHolder, JOSStory

## from opentok import OpenTok

# Create your views here.

User = get_user_model()

@login_required
def personaldesk(request, pk, template="josprojects/jospersonaldesk.html", extra_context=None):
    user = get_object_or_404(User, pk=pk)

    activate('America/Los_Angeles')

    current_profile = get_object_or_404(JOSProfile, user=user)
    weeks = JOSCourseWeek.objects.filter(publish=True).order_by('week_no') # retrieves all weeks available

    context = {"profile": current_profile, "weeks": weeks}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def mystory_list(request, template="josprojects/mystory_list.html", extra_context=None):
    activate('America/Los_Angeles')
    stories = JOSStory.objects.filter(author=request.user).order_by('-updated')

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
@csrf_exempt
def josstory(request, story_id=0, edit=False, template="josprojects/josstory.html", extra_context=None):
    activate('America/Los_Angeles')

    try:
        story = get_object_or_404(JOSStory, pk=story_id)
    except:
        story = JOSStory.objects.create(author=request.user, title="- untitled -", content="- content goes here -")

    try:
        comment_thread = get_object_or_404(JOSMessageThread, subject='Comments: ' + str(story.id))
    except:
        comment_thread = 'missing'

    if comment_thread == 'missing':
        try:
            comment_thread = get_object_or_404(JOSMessageThread, subject='On: ' + story.title)
        except:
            comment_thread = JOSMessageThread.objects.create(subject='On: ' + story.title)
            comment_thread.save()

    comments = Message.objects.filter(message_thread=comment_thread).order_by('sent_at')

    new_permission_value = int(request.GET.get('pubperm', 0))
    if new_permission_value != 0:
        story.publish_permission = new_permission_value
        story.save()

        if new_permission_value == 1:
            permission_change_message = 'only you can read it'
        elif new_permission_value == 2:
            permission_change_message = 'your team can read it'
        else:
            permission_change_message = 'the community can read it'

        info(request, "Sharing changed, now: " + permission_change_message + "!")
        return redirect('joinourstory.com/josstory/' + str(story_id))

    if request.method == 'POST':
        nu_content = request.POST['nucontent']
        field_to_edit = request.POST['field_to_edit']

        if field_to_edit == "comment":
            send_message = Message.objects.create(
                body = nu_content,
                message_thread = comment_thread,
                recipient = story.author,
                sender = request.user,
                sent_at =timezone.now()
            )
            send_message.save()

            info(request, "Great thought, thanks!")

        else:
            ckrtf_holder = CKRichTextHolder.objects.create(
                author = request.user,
                parent_class = 'JOSStory',
                parent_id = story.id,
                field_edited = field_to_edit,
                content = getattr(story, field_to_edit)
            )
            ckrtf_holder.save()

            setattr(story, field_to_edit, nu_content)
            info(request, "Changes saved!")
            story.save()

        edit = False

        return redirect('joinourstory.com/josstory/' + str(story_id))

    context = {'story': story, 'edit': edit, "comments": comments}
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


def temasystest(request, incognito=False, jos_id=0, template="josprojects/temasys_test.html"):
    JOSKey = 'e18f2a1f-f608-44ae-8fc9-e2a42bb0278e'
    try:
        user = get_object_or_404(User, pk=jos_id)
        josname = user.JOSProfile.jos_name()
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

