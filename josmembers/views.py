### josmembers/views.py
from __future__ import unicode_literals

from django.contrib.auth import (login as auth_login, logout as auth_logout, authenticate, get_user_model)
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, error
from django.core.urlresolvers import NoReverseMatch
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

from mezzanine.accounts import get_profile_form
from mezzanine.accounts.forms import PasswordResetForm
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import login_redirect, next_url

from cloudinary.forms import cl_init_js_callbacks

from .models import JOSProfile, CKRichTextHolder
from .forms import JOSSignupForm, JOSNewPasswordForm, CKRichTextEditForm

User = get_user_model()

### Profiles:

@login_required
def josprofile_update(request, template="josmembers/josmembers_josprofile_update.html",
                   extra_context=None):
    """
    Profile update form.
    """
    context = {}
    profile_form = get_profile_form()
    form = profile_form(request.POST or None, request.FILES or None, instance=request.user)
    #cl_init_js_callbacks(form, request)
    if request.method == "POST" and form.is_valid():
        if request.POST.get['temp_profile_image']:
            form.fields['profile_image']=request.POST.get['temp_profile_image']
        user = form.save()
        info(request, _("Profile changed"))
        try:
            return redirect("profile", username=user.username)
        except NoReverseMatch:
            return redirect("profile_update")
    context.update({"form": form, "title": _("Change Profile")})
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


@login_required
def josprofile_redirect(request):
    """
    Just gives the URL prefix for profiles an action - redirect
    to the logged in user's profile.
    """
    return redirect("profile", username=request.user.username)

### Signup:

def signup(request, template="accounts/account_signup.html", extra_context=None):
    """
    Signup form.
    """
    remote_address = request.META.get('HTTP_X_REAL_IP')
    signup_form = JOSSignupForm
    form = signup_form(request.POST or None, request.FILES or None)
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
    context.update ({"remote_address": remote_address})
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

### Passwords:

def password_reset(request, template="accounts/account_password_reset.html",
                       form_class=PasswordResetForm, extra_context=None):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        send_verification_mail(request, user, "password_reset_verify")
        info(request, _("Email with password reset link sent"))
    context = {"form": form, "title": _("Password Reset")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def password_reset_verify(request, uidb36=None, token=None):
    user = authenticate(uidb36=uidb36, token=token, is_active=True)

    if user is not None:
        auth_login(request, user)
        return redirect('jos_new_password')

    else:
        error(request, _("This link has expired. Please enter your email address again"))
        return redirect("jos_password_reset")


def jos_new_password(request, template="josmembers/josmembers_jospassword_reset.html", extra_context=None):

    # user_id = request.user.id
    # info(request, _(user_id))
    form = JOSNewPasswordForm(instance=request.user)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = JOSNewPasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            info(request, _("Password Changed"))
            return redirect("/")

    context = {"form": form, "title": _("Reset password")}
    return TemplateResponse(request, template, context)


def logout(request):
    """
    Log the user out.
    """
    auth_logout(request)
    info(request, _("Successfully logged out - come back soon"))
    return redirect("/")


def josprofile(request, username, edit, template="josmembers/josmembers_josprofile.html", extra_context=None):
    """
    Display a profile.
    """
    lookup = {"username__iexact": username, "is_active": True}
    user = get_object_or_404(User, **lookup)
    currentProfile = get_object_or_404(JOSProfile, user=user)

    try:
        field_to_edit = request.GET['field_to_edit']
    except:
        field_to_edit = "nofield"

    if field_to_edit != "nofield":
        content = getattr(currentProfile, field_to_edit)
        ckrtfholder = CKRichTextHolder.objects.create(author=user, field_to_edit=field_to_edit, content=content)
        pk = ckrtfholder.pk
        query_string = "/?pk=" + str(pk)
        return redirect("ckrichtextedit" + query_string)
    else:
        content = "nocontent"
        pk = 0

    context = {"profile": currentProfile, "edit": edit}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)

### Writing Utilities

def ckrichtextedit(request, template="josmembers/ckrichtextedit.html", extra_context=None):

    try:
        pk = request.GET['pk']
        instance = get_object_or_404(CKRichTextHolder, pk=pk)
        author = instance.author.get_full_name()
        field_to_edit = instance.field_to_edit.replace('_', ' ')
        title = instance.title
        form = CKRichTextEditForm(instance=instance)
    except:
        author = "noauthor"
        field_to_edit = "nofield"
        title = "notitle"
        form = CKRichTextEditForm()

    context = {'form': form, 'author': author, 'field_to_edit': field_to_edit, 'title': title}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)