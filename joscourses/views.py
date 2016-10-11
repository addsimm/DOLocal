from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from .models import JOSCourseWeek, JOSHandout

# Create your views here.

@login_required
def course_week_list(request, template="###", extra_context=None):
    weeks = JOSCourseWeek.objects.order_by('week_no')

    context = {'weeks': weeks}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def course_week(request, week_no="0", part_no="9", segment_no="9", handout_id="1", template="joscourses/joshandout.html", extra_context=None):

    week = get_object_or_404(JOSCourseWeek, week_no=1)
    handouts = JOSHandout.objects.filter(courseweek=week, part_no = part_no, publish=True).order_by('segment_no', 'element_order')
    segments = handouts.distinct().order_by('segment_no')

### need handouts for segment


    try:
        segment_no = segments[0].segment_no
    except:
        segment_no = 9

    try:
        handout = handouts[0]
    except:
        handout = get_object_or_404(JOSHandout, pk=1)

    if not handout.pdf_handout:
        handout.pdf_handout = 'missing'

    current_segment_no = handout.segment_no
    current_segment = get_object_or_404(segments, segment_no=current_segment_no)

    context = { 'week':       week,
                'segment_no': segment_no,
                'handout_id': handout_id,
                'segments':   segments,
                'current_segment': current_segment,
                'handouts':   handouts,
                'handout':    handout
               }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


def next_handout(request, extra_context=None):
    week_no = request.GET['week_no']
    next_order = int(request.GET['order'])

    week = get_object_or_404(JOSCourseWeek, pk=week_no)
    handouts =JOSHandout.objects.filter(courseweek=week, publish=True).order_by('element_order')

    try:
        next_handout_id = str(handouts[next_order].id)
    except:
        next_handout_id = str(handouts[0].id)

    return redirect("http://www.joinourstory.com/joscourses/handout/" + next_handout_id)