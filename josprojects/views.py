from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from josmembers.models import JOSProfile

from .models import CKRichTextHolder, JOSStory
from .forms import CKRichTextEditForm, JOSStoryForm

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


@csrf_exempt
def ckrichtextedit(request, pk, template="josprojects/ckrichtextedit.html", extra_context=None):
    instance = get_object_or_404(CKRichTextHolder, pk=pk)
    form = CKRichTextEditForm(instance=instance)

    if request.method == 'POST':
        content = request.POST['content']
        instance.content = content
        instance.save()
        query_string = "/?pk=" + pk

        return redirect("/users/" + str(instance.author_id) + query_string)

    context = {'form': form}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def mystory(request, pk=0, template="josprojects/mystory.html", extra_context=None):

    if pk == 0:
        story = JOSStory(author=request.user)
    else:
        story = get_object_or_404(JOSStory, pk=pk)

    context = {'story': story}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def mystory_list(request, pk=0, template="josprojects/mystory_list.html", extra_context=None):

    stories = JOSStory.objects.filter(author=request.user)

    context = {'stories': stories}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)
