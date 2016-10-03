from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from .models import JOSCourseWeek, JOSHandout

# Create your views here.

@login_required
def course_week_list(request, template="###", extra_context=None):
    weeks = JOSCourseWeek.objects.order_by('weekno')

    context = {'weeks': weeks}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def course_week(request, weekid=0, template="joscourses/joscourseweek.html", extra_context=None):
    week = get_object_or_404(JOSCourseWeek, pk=weekid)
    handouts = JOSHandout.objects.filter(courseweek=week, publish=True).order_by('segment_order')
    try:
        handout = handouts[0]
        handno = str(handout.id)
    except:
        handout = "missing"
        handno = 0

    return redirect("http://www.joinourstory.com/joscourses/handout/" + str(handno))


@login_required
@csrf_exempt
def handout(request, handoutid=0, edit=False, template="joscourses/joshandout.html", extra_context=None):

    # default_week = get_object_or_404(JOSCourseWeek, pk=10)
    try:
        handout = get_object_or_404(JOSHandout, pk=handoutid)
    except:
        handout = get_object_or_404(JOSHandout, pk=1)

    handouts = JOSHandout.objects.filter(courseweek=handout.courseweek, publish=True).order_by('segment_order')

    if not handout.pdf_handout:
        handout.pdf_handout = 'missing'

    context = {'week': handout.courseweek,
               'handouts': handouts,
               'handout': handout,
               'handoutid': handoutid}

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


def nexthandout(request, extra_context=None):
    weekid = request.GET['weekid']
    nextorder = int(request.GET['order'])

    week = get_object_or_404(JOSCourseWeek, pk=weekid)
    handouts =JOSHandout.objects.filter(courseweek=week, publish=True).order_by('segment_order')

    try:
        next_handout_id = str(handouts[nextorder].id)
    except:
        next_handout_id = str(handouts[0].id)

    return redirect("http://www.joinourstory.com/joscourses/handout/" + next_handout_id)


    # publish_handout = request.GET.get('pub', None)
    # if publish_handout != None:
    #     if publish_handout == 'publish':
    #         handout.publish = True
    #         info(request, handout.title + " -- has been shared!")
    #     elif publish_handout == 'remove':
    #         handout.publish = False
    #         info(request, handout.title + " -- is now hidden.")
    #     handout.save()
    #
    # if request.method == 'POST':
    #     nucontent = request.POST['nucontent']
    #     field_to_edit = request.POST['field_to_edit']
    #
    #     setattr(handout, field_to_edit, nucontent)
    #     handout.save()
    #
    #     edit = False