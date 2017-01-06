import os.path
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.timezone import activate
from django.views.decorators.csrf import csrf_exempt

from wand.image import Image
from josmessages.models import Message, JOSMessageThread
from .models import *

### UNUSED
@login_required
def course_week_list(request, template="###", extra_context=None):
    weeks = JOSCourseWeek.objects.order_by('week_no')

    context = {'weeks': weeks}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def course_week(request, week_no="0", part_no="9", segment_no="9", handout_id="1",
                template="joscourses/joshandout.html", extra_context=None):

    week = get_object_or_404(JOSCourseWeek, week_no=int(week_no))
    week_handouts = JOSHandout.objects.filter(courseweek=week, part_no=int(part_no), publish=True)
    week_segments = week_handouts.distinct('segment_no').order_by('segment_no')

    try:
        first_segment_no = week_segments[0].segment_no
    except:
        first_segment_no = 9

    if segment_no != "9":
        current_segment_no = int(segment_no)
    else:
        current_segment_no = first_segment_no

    current_handouts = week_handouts.filter(segment_no=current_segment_no).order_by('element_order')

    if handout_id == '1':
        try:
            cur_handout = current_handouts[0]
        except:
            cur_handout = get_object_or_404(JOSHandout, pk=1)
    else:
        try:
            cur_handout = get_object_or_404(JOSHandout, pk=int(handout_id))
        except:
            cur_handout = get_object_or_404(JOSHandout, pk=1)

    pdf_missing = False
    if not cur_handout.pdf_handout:
        pdf_missing = True

    f_name = ' '
    ### change to image
    if cur_handout.pdf_handout:
        if os.path.isfile(cur_handout.pdf_handout.path):
            with Image(filename=cur_handout.pdf_handout.path) as original:
                with original.convert('png') as converted:
                    f_name = 'static/img/temp' + str(request.user.id) + '.png'
                    with open(f_name, 'wb') as f:
                        converted.save(file=f)

    context = {
        'week':            week,
        'part_no':         int(part_no),
        'segments':        week_segments,
        'current_segment': current_segment_no,
        'handouts':        current_handouts,
        'handout':         cur_handout,
        'pdf_missing':     pdf_missing,
        'f_name':          f_name,
        'download_filename': "BetterStorytelling-Handout-" + str(cur_handout.id)

    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def josstory(request, story_id=0, edit=False, template="joscourses/jos_story.html", extra_context=None):
    activate('America/Los_Angeles')

    try:
        story = get_object_or_404(JOSStory, pk=story_id)
    except:
        story = JOSStory.objects.create(author=request.user, title="- Untitled -", story_content="- Enter content here -")
        JOSPriorVersion.objects.create(
                pv_story=story,
                pv_title=story.title,
                pv_story_content=story.story_content
        )

    if not story.wheel:
        wheel = JOSWheel.objects.create()
        wheel.save()
        story.wheel = wheel
        story.save()

    if not story.message_thread:
        story.message_thread = JOSMessageThread.objects.create(subject=story.title)
        story.save()

    if not story.wheel.plot:
        story.wheel.plot = JOSPlot.objects.create()
        story.wheel.save()

    if not story.wheel.character:
        story.wheel.character = JOSCharacter.objects.create()
        story.wheel.save()

    if not story.wheel.conflict:
        story.wheel.conflict = JOSConflict.objects.create()
        story.wheel.save()

    if not story.wheel.world:
        story.wheel.world = JOSWorld.objects.create()
        story.wheel.save()

    if not story.wheel.theme:
        story.wheel.theme = JOSTheme.objects.create()
        story.wheel.save()

    comments = Message.objects.filter(message_thread=story.message_thread).order_by('sent_at')
    prior_versions = JOSPriorVersion.objects.filter(pv_story=story).order_by('-pv_date')

    new_title = request.GET.get('newtitle', 'none')
    if new_title != 'none':
        story.title = new_title
        story.save()

        title_message = 'Story title changed to: ' + new_title

        info(request, title_message)
        return redirect('joinourstory.com/josstory/' + str(story_id))

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

    new_auto_save_value = request.GET.get('autosave', 'none')
    if new_auto_save_value != 'none':
        story.auto_save = new_permission_value
        story.save()

        if new_auto_save_value == 'True':
            auto_save_message = 'Auto save is now on!'
        else:
            auto_save_message = 'Warning: auto save is off!'

        info(request, auto_save_message)
        return redirect('joinourstory.com/josstory/' + str(story_id))

    context = {'story': story, 'edit': edit, "prior_versions": prior_versions, "comments": comments}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
@csrf_exempt
def ajax_story_update(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('not ok')

    story_id = int(request.get_full_path().split('=')[1])

    story = ' '
    try:
        story = get_object_or_404(JOSStory, pk=story_id)
    except:
        info(request, "Cannot find story!")

    comment_thread = story.message_thread

    new_content = request.POST.get('new_content', 'missing')
    section = request.POST.get('section', 'missing')

    if new_content != 'missing':

        if section == 'story_content':

            # Prior versions logic
            new_version = JOSPriorVersion(
                    pv_story=story,
                    pv_title=story.title,
                    pv_story_content=story.story_content
            )
            new_version.save()
            prior_versions = JOSPriorVersion.objects.filter(pv_story=story).order_by('-pv_date')
            new_date = prior_versions[0].pv_date

            try:
                latest_date = prior_versions[1].pv_date
                since_last = new_date - latest_date
            except:
                info(request, 'problem')
                return

            if len(prior_versions) > 4:
                if since_last > timedelta(seconds=3660):
                    JOSPriorVersion.objects.filter(pv_story=story).earliest('pv_date').delete()
                else:
                    new_version.delete()

            story.story_content = new_content
            story.save()
            info(request, "Story saved!")

        elif section == 'title':
            story.title = new_content
            story.save()


        elif section == "comment":
            send_message = Message.objects.create(
                    body=new_content,
                    message_thread=comment_thread,
                    recipient=story.author,
                    sender=request.user,
                    sent_at=timezone.now()
            )
            send_message.save()
            info(request, "Great thought, thanks!")

    return HttpResponse(story_id)


@login_required
def joswheel(request, wheel_id=0, template="joscourses/wheel.html", extra_context=None):
    activate('America/Los_Angeles')

    try:
        wheel = get_object_or_404(JOSWheel, pk=wheel_id)
    except:
        wheel = JOSWheel.objects.create(author=request.user, title="- Untitled -")
        wheel.save()

    context = {'wheel' : wheel}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def sw_plot(request, wheel_id=0, edit=False, template="joscourses/sw-plot.html", extra_context=None):

    try:
        wheel = get_object_or_404(JOSWheel, pk=int(wheel_id))
    except:
        return HttpResponse('cant find wheel: ' + str(wheel_id))

    context = {
        'plot': wheel.plot,
        'wheel': wheel,
        'edit': edit
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def sw_world(request, wheel_id=0, edit=False, template="joscourses/sw-world.html", extra_context=None):
    try:
        wheel = get_object_or_404(JOSWheel, pk=int(wheel_id))
    except:
        return HttpResponse('cant find wheel: ' + str(wheel_id))

    context = {
        'world': wheel.world,
        'wheel': wheel,
        'edit':  edit
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def sw_theme(request, wheel_id=0, edit=False, template="joscourses/sw-theme.html", extra_context=None):
    try:
        wheel = get_object_or_404(JOSWheel, pk=int(wheel_id))
    except:
        return HttpResponse('cant find wheel: ' + str(wheel_id))

    context = {
        'theme': wheel.theme,
        'wheel': wheel,
        'edit':  edit
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def sw_conflict(request, wheel_id=0, edit=False, template="joscourses/sw-conflict.html", extra_context=None):
    try:
        wheel = get_object_or_404(JOSWheel, pk=int(wheel_id))
    except:
        return HttpResponse('cant find wheel: ' + str(wheel_id))

    context = {
        'conflict': wheel.conflict,
        'wheel':    wheel,
        'edit':     edit
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
@csrf_exempt
def ajax_wheel_update(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('not ajax post')

    wheel_id = int(request.get_full_path().split('=')[1])

    try:
        wheel = get_object_or_404(JOSWheel, pk=wheel_id)
    except:
        return HttpResponse("Error JOSWheel missing, please call us")

    central_new_content = request.POST.get('central_new_content', 'missing')
    sw_template = request.POST.get('sw_template', 'missing')
    template_section = request.POST.get('template_section', 'missing')
    action = request.POST.get('action', 'missing')
    character_id = request.POST.get('character_id', 'missing')

    template = ' '
    if sw_template == 'plot':
        try:
            template = wheel.plot
        except:
            return HttpResponse('Error JOSPlot missing, please call us')

        setattr(template, template_section, central_new_content)
        template.save()

    elif sw_template == 'characters':
        if action == 'delete':
            try:
                character = get_object_or_404(JOSCharacter, pk=int(character_id))
            except:
                return HttpResponse("Error JOSCharacter missing, please call us")

            character.delete()
            info(request, "Character deleted!")
            return HttpResponse('deleted character: ' + str(character_id))

    return HttpResponse('ok')


def sw_characters(request, wheel_id=0, character_id=0, edit=False, template="joscourses/sw-characters.html", extra_context=None):
    wheel = get_object_or_404(JOSWheel, pk=int(wheel_id))

    if int(character_id) == 1:
        character = JOSCharacter.objects.create()
        character.joswheel_set.add(wheel)

    all_characters = JOSCharacter.objects.filter(wheel=wheel)

    if not all_characters:
        character = None
    else:
        try:
            character = get_object_or_404(JOSCharacter, pk=int(character_id))
        except:
            character = all_characters[0]

    context = {
        'character': character,
        'all_characters': all_characters,
        'wheel': wheel,
        'edit': edit
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def story_reader(request, story_id=0, template="joscourses/story_reader.html", extra_context=None):

    try:
        story = get_object_or_404(JOSStory, pk=story_id)
    except:
        return HttpResponse('Sorry, story not found.')

    comments = Message.objects.filter(message_thread=story.message_thread).order_by('sent_at')

    context = {
        'story': story,
        'comments': comments
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)