from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from django.contrib.auth import (login as auth_login, authenticate,
                                 logout as auth_logout, get_user_model)
from django.contrib.auth.decorators import login_required

from josaccounts.models import JOSProfile

User = get_user_model()

# Create your views here.

def josprofile(request, username, template="josaccounts/josaccounts_josprofile.html", extra_context=None): ### CHANGE
    """
    Display a profile.
    """
    lookup = {"username__iexact": username, "is_active": True}
    user = get_object_or_404(User, **lookup)
    currentProfile = get_object_or_404(JOSProfile, user=user)
    context = {"profile_user": user}
    context.update({"about_me": currentProfile.about_me,
                    "profile_photo": currentProfile.profile_photo})
    return TemplateResponse(request, template, context)


### Original Profile View
# def profile(request, username, template="accounts/account_profile.html",
#                 extra_context=None):
#     """
#     Display a profile.
#     """
#     lookup = {"username__iexact": username, "is_active": True}
#     context = {"profile_user": get_object_or_404(User, **lookup)}
#     context.update(extra_context or {})
#     return TemplateResponse(request, template, context)