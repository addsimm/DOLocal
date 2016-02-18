from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.contrib.auth import (login as auth_login, authenticate,
                                 logout as auth_logout, get_user_model)

from josmembers.models import JOSProfile

User = get_user_model()

# Create your views here.

def josprofile(request, username, template="josmembers/josmembers_josprofile.html", extra_context=None):
    """
    Display a profile.
    """
    lookup = {"username__iexact": username, "is_active": True}
    user = get_object_or_404(User, **lookup)
    currentProfile = get_object_or_404(JOSProfile, user=user)
    context = {"profile_user": user}
    context.update({"profile": currentProfile,
                    "profile_photo": JOSProfile.profile_photo})

    return TemplateResponse(request, template, context)
