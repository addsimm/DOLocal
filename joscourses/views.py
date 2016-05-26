from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from josmembers.models import JOSProfile
from joscourses.models import JOSCourseWeek

from .models import JOSCourseWeek

from josprojects.models import CKRichTextHolder
from josprojects.forms import CKRichTextEditForm

# Create your views here.

@login_required
def course_week_list(request, template="josprojects/mystory_list.html", extra_context=None):
    weeks = JOSCourseWeek.objects.all()

    context = {'weeks': weeks}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def course_week(request, weekid=0, edit=False, template="joscourses/joscourseweek.html", extra_context=None):
    try:
        week = get_object_or_404(JOSCourseWeek, pk=weekid)
    except:
        week = JOSCourseWeek.objects.create(author=request.user,
                                        title="Untitled",
                                        content="Coming soon")

    publish = request.GET.get('pub', None)
    if publish != None:
        if publish == 'publish':
            week.publish = True
            info(request, week.week_title + " -- has been published!")
        elif publish == 'remove':
            week.publish = False
            info(request, week.week_title + " -- is now hidden.")
        week.save()

    field_to_edit = request.GET.get('field_to_edit', "nofield")
    if field_to_edit != "nofield":
        content = getattr(week, field_to_edit)

        ckrtfholder = CKRichTextHolder.objects.create(
            author=request.user,
            title=week.title,
            field_to_edit=field_to_edit,
            content=content)

        nexturl = 'joscourses/courseweek/' + str(week.id) + '/?pk=' + str(ckrtfholder.pk)
        ckrtfholder.nextURL = nexturl
        ckrtfholder.save()

        query_string = "/" + str(ckrtfholder.pk)

        return redirect("/ckrichtextedit" + query_string)

    pk = request.GET.get('pk', None)
    if pk != None:
        ckrtfholder = get_object_or_404(CKRichTextHolder, pk=pk)
        content = ckrtfholder.content
        if ckrtfholder.field_to_edit != "title":
            week.content = content
        else:
            week.title = content.strip()
        week.save()

    context = {'week': week,
               'edit': edit,
               'field_to_edit': field_to_edit}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)

