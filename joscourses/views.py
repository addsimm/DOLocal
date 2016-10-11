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
    week_handouts = JOSHandout.objects.filter(courseweek=week, part_no = int(part_no), publish=True)
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

    context = { 'week':       week,
                'part_no': int(part_no),
                'segments':   week_segments,
                'current_segment': current_segment_no,
                'handouts':   current_handouts,
                'handout': cur_handout,
                'pdf_missing': pdf_missing
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