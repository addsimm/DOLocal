import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import activate

from joscourses.models import JOSCourseWeek
from josmembers.models import JOSProfile
from josmessages.models import Message, JOSMessageThread

from .models import CKRichTextHolder, JOSStory

from opentok import OpenTok

# Create your views here.

User = get_user_model()

@login_required
def personaldesk(request, pk, template="josprojects/jospersonaldesk.html", extra_context=None):
    user = get_object_or_404(User, pk=pk)

    activate('America/Los_Angeles')

    currentProfile = get_object_or_404(JOSProfile, user=user)
    weeks = JOSCourseWeek.objects.filter(publish=True).order_by('weekno') # retrives all weeks available

    context = {"profile": currentProfile, "weeks": weeks}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)

@login_required
def mystory_list(request, template="josprojects/mystory_list.html", extra_context=None):
    stories = JOSStory.objects.filter(author=request.user)

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)

@login_required
@csrf_exempt
def josstory(request, storyid=0, edit=False, template="josprojects/josstory.html", extra_context=None):

    try:
        story = get_object_or_404(JOSStory, pk=storyid)
    except:
        story = JOSStory.objects.create(author=request.user, title="Untitled", content="Coming soon")

    try:
        comment_thread = get_object_or_404(JOSMessageThread, subject='Comments: ' + str(story.id))
    except:
        comment_thread = JOSMessageThread.objects.create(subject='Comments: '+ str(story.id))

    comments = Message.objects.filter(message_thread=comment_thread).order_by('sent_at')

    publish_story = request.GET.get('pub', None)
    if publish_story != None:
        if publish_story == 'publish':
            story.publish = True
            info(request, story.title + " -- has been shared!")
        elif publish_story == 'remove':
            story.publish = False
            info(request, story.title + " -- is now hidden.")
        story.save()

    if request.method == 'POST':
        nucontent = request.POST['nucontent']
        field_to_edit = request.POST['field_to_edit']

        if field_to_edit == "comment":
            message = Message.objects.create(
                body = nucontent,
                is_last = True,
                message_thread = comment_thread,
                recipient = story.author,
                sender = request.user,
                sent_at = datetime.datetime.now().time()
            )
            message.save()
            ct_mc = comment_thread.message_count
            comment_thread.last_message_id = message.id
            comment_thread.last_recipient = story.author
            comment_thread.message_count = ct_mc + 1
            comment_thread.save()
            info(request, "Great thought, thanks!")

        else:
            ckrtfholder = CKRichTextHolder.objects.create(
                author = request.user,
                parent_class = 'JOSStory',
                parent_id = story.id,
                field_edited = field_to_edit,
                content = getattr(story, field_to_edit)
            )
            ckrtfholder.save()

            setattr(story, field_to_edit, nucontent)
            info(request, "Changes saved!")
            story.save()

        edit = False

    context = {'story': story, 'edit': edit, "comments": comments}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def story_gallery(request, template="josprojects/story_gallery.html", extra_context=None):
    stories = JOSStory.objects.filter(publish=True).order_by('updated')

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


def tokboxtest(request, template="demotokbox.html"):
    APIKey = '45616422'
    secretkey = '7deb719076852b32e72682b2f19b732f35bf5ecf'

    opentok = OpenTok(APIKey, secretkey)

    jos_name = request.user.JOSProfile.jos_name()

    connectionMetadata = jos_name
    # session = opentok.create_session()
    # session_id = session.session_id

    session_id = '1_MX40NTYxNjQyMn5-MTQ2Nzc2MzI4OTQ2M341SHRLYnhibWJGRzMySTZkZnA5QTJhYzB-fg'
    token = opentok.generate_token(session_id=session_id, data=connectionMetadata)

    context = {
        'apikey':     APIKey,
        'session_id': session_id,
        'token':      token,
    }

    return TemplateResponse(request, template, context)




