from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from josmembers.models import JOSProfile
from joscourses.models import JOSCourseWeek

from .models import JOSCourseWeek, JOSHandout

from josprojects.models import CKRichTextHolder
from josprojects.forms import CKRichTextEditForm

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

    context = {'week': week,
               'handouts': handouts}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def handout(request, handoutid=0, template="joscourses/joshandout.html", extra_context=None):
    handout = get_object_or_404(JOSHandout, pk=handoutid)

    context = {'handout': handout}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)
