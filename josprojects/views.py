from django.shortcuts import render

# Create your views here.

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import info
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from mezzanine.core.forms import Html5Mixin

from josmembers.models import JOSProfile
from joscourses.models import JOSCourseWeek

from .models import CKRichTextHolder, JOSStory

User = get_user_model()

@login_required
def personaldesk(request, pk, template="josprojects/jospersonaldesk.html", extra_context=None):
    user = get_object_or_404(User, pk=pk)
    currentProfile = get_object_or_404(JOSProfile, user=user)

    weeks = JOSCourseWeek.objects.order_by('weekno') # retrives all weeks available

    context = {"profile": currentProfile,
               "weeks": weeks}
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

    user = request.user

    try:
        story = get_object_or_404(JOSStory, pk=storyid)
    except:
        story = JOSStory.objects.create(author=user,
                                        title="Untitled",
                                        content="Coming soon")

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
        setattr(story, field_to_edit, nucontent)
        info(request, "Changes saved!")
        story.save()

        context = {'story': story, 'edit': 'false'}
        context.update(extra_context or {})

        #return TemplateResponse(request, template, context)
        redirect("/")

    form = None

    ckrtfholder = None
    pk4ckeditor = 0
    field_to_edit = request.GET.get('field_to_edit', "nofield")
    if field_to_edit != "nofield":
        content = getattr(story, field_to_edit)
        ckrtfholder = CKRichTextHolder.objects.create(
            author=request.user,
            class_to_edit = 'story',
            id_to_edit = story.id,
            field_to_edit=field_to_edit,
            content=content
        )
        pk4ckeditor = ckrtfholder.pk4ckeditor = ckrtfholder.id
        ckrtfholder.save()

    context = {'story': story, 'edit': edit, 'field_to_edit': field_to_edit, 'pk4ckeditor': pk4ckeditor}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def story_gallery(request, template="josprojects/story_gallery.html", extra_context=None):
    stories = JOSStory.objects.filter(publish=True)

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


# @csrf_exempt
# def ckrichtextedit(request, pk, template="josprojects/ckrichtextedit.html", extra_context=None):
#     instance = get_object_or_404(CKRichTextHolder, pk=pk)
#     form = CKRichTextEditForm(instance=instance)
#
#     if request.method == 'POST':
#         content = request.POST['content']
#         instance.content = content
#         instance.save()
#
#         return redirect(instance.nextURL)
#
#     context = {'form': form}
#     context.update(extra_context or {})
#
#     return TemplateResponse(request, template, context)


