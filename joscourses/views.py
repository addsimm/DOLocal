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
def course_week(request, week_no=0, part='none', template="joscourses/joscourseweek.html", extra_context=None):
    if part == 'part1':
        part_filter = 1
    elif part == 'part2':
        part_filter = 2
    else:
        part_filter = 0
    week = get_object_or_404(JOSCourseWeek, pk=week_no)
    handouts = JOSHandout.objects.filter(courseweek=week, part_no = part_filter, publish=True).order_by('element_order')
    try:
        handout = handouts[0]
        hand_no = str(handout.id)
    except:
        hand_no = 1

    return redirect("http://www.joinourstory.com/joscourses/handout/" + str(hand_no))


@login_required
def handout(request, handout_id=0, edit=False, template="joscourses/joshandout.html", extra_context=None):

    # default_week = get_object_or_404(JOSCourseWeek, pk=10)
    try:
        handout = get_object_or_404(JOSHandout, pk=handout_id)
    except:
        handout = get_object_or_404(JOSHandout, pk=1)

    part_filter = handout.part_no

    handouts = JOSHandout.objects.filter(courseweek=handout.courseweek, part_no=part_filter, publish=True).order_by('element_order')

    if not handout.pdf_handout:
        handout.pdf_handout = 'missing'

    context = {'week': handout.courseweek,
               'handouts': handouts,
               'handout': handout,
               'handout_id': handout_id}

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