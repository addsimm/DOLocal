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
    handouts = JOSHandout.objects.filter(courseweek=week).order_by('handoutno')
    context = {'week': week, 'handouts': handouts}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
@csrf_exempt
def handout(request, handoutid=0, edit=False, template="joscourses/joshandout.html", extra_context=None):

    default_week = get_object_or_404(JOSCourseWeek, pk=10)
    try:
        handout = get_object_or_404(JOSHandout, pk=handoutid)
    except:
        handout = JOSHandout.objects.create(course_week = default_week,
                                            title="Untitled",
                                            content="Coming soon")

    publish_handout = request.GET.get('pub', None)
    if publish_handout != None:
        if publish_handout == 'publish':
            handout.publish = True
            info(request, handout.title + " -- has been shared!")
        elif publish_handout == 'remove':
            handout.publish = False
            info(request, handout.title + " -- is now hidden.")
        handout.save()

    if request.method == 'POST':
        nucontent = request.POST['nucontent']
        field_to_edit = request.POST['field_to_edit']

        setattr(handout, field_to_edit, nucontent)
        handout.save()

        edit = False

    context = {'handout': handout, 'edit': edit}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)
