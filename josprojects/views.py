from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from josmembers.models import JOSProfile

from .models import CKRichTextHolder, JOSStory
from .forms import CKRichTextEditForm

User = get_user_model()

@login_required
def personaldesk(request, pk, template="josprojects/jospersonaldesk.html", extra_context=None):
    user = get_object_or_404(User, pk=pk)
    currentProfile = get_object_or_404(JOSProfile, user=user)

    instance = None

    if instance:
        form = CKRichTextEditForm(instance=instance)
    else:
        form = CKRichTextEditForm()

    if request.method == 'POST' and instance:
        content = request.POST['content']
        instance.content = content
        instance.save()
        username = str(instance.author)
        query_string = "/?pk=" + pk

        return redirect("/users/" + username + query_string)

    context = {"profile": currentProfile}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def mystory_list(request, template="josprojects/mystory_list.html", extra_context=None):
    stories = JOSStory.objects.filter(author=request.user)

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def story_gallery(request, template="josprojects/story_gallery.html", extra_context=None):
    stories = JOSStory.objects.filter(publish=True)

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@csrf_exempt
def ckrichtextedit(request, pk, template="josprojects/ckrichtextedit.html", extra_context=None):
    instance = get_object_or_404(CKRichTextHolder, pk=pk)
    form = CKRichTextEditForm(instance=instance)

    if request.method == 'POST':
        content = request.POST['content']
        instance.content = content
        instance.save()

        return redirect(instance.nextURL)

    context = {'form': form}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def josstory(request, storyid=0, edit=False, template="josprojects/josstory.html", extra_context=None):

    try:
        story = get_object_or_404(JOSStory, pk=storyid)
    except:
        story = JOSStory.objects.create(author=request.user,
                                        title="Untitled",
                                        content="Coming soon")

    publish = request.GET.get('pub', None)
    if publish != None:
        if publish == 'publish':
            story.publish = True
            info(request, story.title + " -- has been shared!")
        elif publish == 'remove':
            story.publish = False
            info(request, story.title + " -- is now hidden.")
        story.save()

    field_to_edit = request.GET.get('field_to_edit', "nofield")
    if field_to_edit != "nofield":
        content = getattr(story, field_to_edit)

        ckrtfholder = CKRichTextHolder.objects.create(
            author=request.user,
            title=story.title,
            field_to_edit=field_to_edit,
            content=content)

        nexturl = '/josstory/' + str(story.id) + '/?pk=' + str(ckrtfholder.pk)
        ckrtfholder.nextURL = nexturl
        ckrtfholder.save()

        query_string = "/" + str(ckrtfholder.pk)

        return redirect("/ckrichtextedit" + query_string)

    pk = request.GET.get('pk', None)
    if pk != None:
        ckrtfholder = get_object_or_404(CKRichTextHolder, pk=pk)
        content = ckrtfholder.content
        if ckrtfholder.field_to_edit != "title":
            story.content = content
        else:
            story.title = content.strip()
        story.save()

    context = {'story': story,
               'edit': edit,
               'field_to_edit': field_to_edit}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)