import os.path

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
from .models import JOSCourseWeek, JOSHandout, JOSStory, JOSWheel, JOSPlotTemplate, JOSCharacter

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

### DEVELOPMENT
def playground_view(request, template="playground.html", extra_context=None):
    context = {}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
@csrf_exempt
def josstory(request, story_id=0, edit=False, template="joscourses/jos_story.html", extra_context=None):
    activate('America/Los_Angeles')

    try:
        story = get_object_or_404(JOSStory, pk=story_id)
    except:
        story = JOSStory.objects.create(author=request.user, title="- Untitled -", content="- Content goes here -")

    if not story.message_thread:
        comment_thread = JOSMessageThread.objects.create(subject=story.title)
        story.message_thread = comment_thread
        story.save()
        return redirect('joscourses.views.josstory', story_id=story.id)

    comment_thread = story.message_thread

    if comment_thread.subject != story.title:
        comment_thread.subject = story.title
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

    context = {'story': story, 'edit': edit, "comments": comments}
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

        if section == 'content':
            story.content = new_content
            story.save()
            info(request, "Story content updated!")

        elif section == 'title':
            story.title = new_content
            story.save()
            info(request, "Story title updated!")

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
def storywheel(request, wheel_id=0, template="joscourses/storywheel.html", extra_context=None):
    activate('America/Los_Angeles')

    try:
        storywheel = get_object_or_404(JOSWheel, pk=wheel_id)
    except:
        storywheel = JOSWheel.objects.create(author=request.user, title="- Untitled -")
        storywheel.save()
        return redirect('joinourstory.com/joscourses/storywheel/' + str(storywheel.id))

    context = {'storywheel' : storywheel}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


def sw_plot(request, wheel_id=0, edit=False, template="joscourses/sw-plot.html", extra_context=None):

    try:
        storywheel = get_object_or_404(JOSWheel, pk=int(wheel_id))
    except:
        return HttpResponse('cant find wheel: ' + str(wheel_id))

    try:
        plot_template = get_object_or_404(JOSPlotTemplate, storywheel=storywheel)
    except:
        plot_template = JOSPlotTemplate.objects.create(storywheel=storywheel)
        plot_template.save()

        return redirect('https://joinourstory.com/joscourses/plot_template/' + str(storywheel.id))

    context = {
        'plot_template': plot_template,
        'storywheel': storywheel,
        'edit': edit
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
@csrf_exempt
def ajax_storywheel_update(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponse('not ok')

    cntrl_new_content = request.POST.get('cntrl_new_content', 'missing')
    sw_template = request.POST.get('sw_template', 'missing')
    template_section = request.POST.get('template_section', 'missing')

    storywheel_id = int(request.get_full_path().split('=')[1])

    try:
        storywheel = get_object_or_404(JOSWheel, pk=storywheel_id)
    except:
        return HttpResponse("Error JOSWheel missing, please call us")

    template = ' '
    if sw_template == 'plot':
        try:
            template = get_object_or_404(JOSPlotTemplate, storywheel=storywheel)
        except:
            return HttpResponse('Error JOSPlotTemplate missing, please call us')

        setattr(template, template_section, cntrl_new_content)
        template.save()

    # info(request, "Template updated!")

    return HttpResponse('cntrl_new_content: ' + cntrl_new_content)


def sw_characters(request, wheel_id=0, character_id=0, edit=False, template="joscourses/sw-characters.html", extra_context=None):
    try:
        storywheel = get_object_or_404(JOSWheel, pk=int(wheel_id))
    except:
        return HttpResponse('cant find wheel: ' + str(wheel_id))

    all_characters = JOSCharacter.objects.filter(storywheel=storywheel).order_by('first_name')

    if not all_characters:
        character = JOSCharacter.objects.create(storywheel=storywheel)

    else:
        try:
            character = get_object_or_404(JOSCharacter, pk=int(character_id))
        except:
            character = all_characters[0]

    context = {
        'character': character,
        'all_characters': all_characters,
        'storywheel': storywheel,
        'edit': edit
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


