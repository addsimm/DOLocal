### josmembers/views.py
from __future__ import unicode_literals

from django.contrib.auth import (login as auth_login, authenticate,
                                 logout as auth_logout, get_user_model)
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, error
from django.core.urlresolvers import NoReverseMatch, get_script_prefix
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from mezzanine.accounts import get_profile_form
from mezzanine.accounts.forms import LoginForm, PasswordResetForm
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import login_redirect, next_url

from cloudinary.forms import cl_init_js_callbacks

from .forms import JOSProfileForm
from .models import JOSProfile

User = get_user_model()


# Create your views here.


def upload_prompt(request):
    context = dict(direct_form=JOSProfileForm())
    cl_init_js_callbacks(context['direct_form'], request)
    return render(request, 'upload_prompt.html', context)


import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def direct_upload_complete(request):
    form = JOSProfileForm(request.POST)
    if form.is_valid():
        form.save()
        ret = dict(photo_id=form.instance.id)
    else:
        ret = dict(errors=form.errors)

    return HttpResponse(json.dumps(ret), content_type='application/json')


def josprofile(request, username, template="josmembers/josmembers_josprofile.html", extra_context=None):
    """
    Display a profile.
    """
    lookup = {"username__iexact": username, "is_active": True}
    user = get_object_or_404(User, **lookup)
    currentProfile = get_object_or_404(JOSProfile, user=user)
    context = {"profile_user": user}
    context.update({"profile": currentProfile,
                    "profile_photo": currentProfile.profile_photo})
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def josprofile_update(request, template="josmembers/josmembers_josprofile_update.html",
                   extra_context=None):
    """
    Profile update form.
    """
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None,
                        instance=request.user)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        info(request, _("Profile updated"))
        try:
            return redirect("profile", username=user.username)
        except NoReverseMatch:
            return redirect("profile_update")
    context = {"form": form, "title": _("Update Profile")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@login_required
def josprofile_redirect(request):
    """
    Just gives the URL prefix for profiles an action - redirect
    to the logged in user's profile.
    """
    return redirect("profile", username=request.user.username)

### Original:

def signup(request, template="accounts/account_signup.html",
           extra_context=None):
    """
    Signup form.
    """
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        new_user = form.save()
        if not new_user.is_active:
            if settings.ACCOUNTS_APPROVAL_REQUIRED:
                send_approve_mail(request, new_user)
                info(request, _("Thanks for signing up! You'll receive "
                                "an email when your account is activated."))
            else:
                send_verification_mail(request, new_user, "signup_verify")
                info(request, _("A verification email has been sent with "
                                "a link for activating your account."))
            return redirect(next_url(request) or "/")
        else:
            info(request, _("Successfully signed up"))
            auth_login(request, new_user)
            return login_redirect(request)
    context = {"form": form, "title": _("Sign up")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def signup_verify(request, uidb36=None, token=None):
    """
    View for the link in the verification email sent to a new user
    when they create an account and ``ACCOUNTS_VERIFICATION_REQUIRED``
    is set to ``True``. Activates the user and logs them in,
    redirecting to the URL they tried to access when signing up.
    """
    user = authenticate(uidb36=uidb36, token=token, is_active=False)
    if user is not None:
        user.is_active = True
        user.save()
        auth_login(request, user)
        info(request, _("Successfully signed up"))
        return login_redirect(request)
    else:
        error(request, _("The link you clicked is no longer valid."))
        return redirect("/")


@login_required
def account_redirect(request):
    """
    Just gives the URL prefix for accounts an action - redirect
    to the profile update form.
    """
    return redirect("profile_update")
