### josmembers/views.py
from __future__ import unicode_literals

from django.contrib.auth import (login as auth_login, logout as auth_logout, authenticate, get_user_model)
from django.contrib.auth.decorators import login_required
from django.contrib.messages import info, error
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from mezzanine.accounts.forms import PasswordResetForm, LoginForm
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import login_redirect, next_url

from .models import JOSProfile, CKRichTextHolder
from .forms import JOSSignupForm, JOSNewPasswordForm, CKRichTextEditForm

User = get_user_model()


def login(request, template="accounts/account_login.html",
          form_class=LoginForm, extra_context=None):
        """
        Login form.
        """
        form = form_class(request.POST or None)
        if request.method == "POST" and form.is_valid():
            authenticated_user = form.save()
            info(request, _("Successfully logged in"))
            auth_login(request, authenticated_user)
            pk = str(authenticated_user.id)
            return redirect("/personaldesk/" + pk)

        context = {"form": form, "title": _("Log in")}
        context.update(extra_context or {})
        return TemplateResponse(request, template, context)


def logout(request):
    """
    Log the user out.
    """
    auth_logout(request)
    info(request, _("Successfully logged out - come back soon"))
    return redirect("/")


### Profiles:

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



def josprofile(request, userid, edit, template="josmembers/josmembers_josprofile.html", extra_context=None):
    """
    Display a profile.
    """
    user = User.objects.get(id=userid)
    username = user.username
    currentProfile = get_object_or_404(JOSProfile, user=user)

    pk = request.GET.get('pk', None)
    field_to_edit = request.GET.get('field_to_edit', "nofield")
    new_image = request.GET.get('new_image', False)

    def getPotentialNewProfileImageIdStr():
        import re
        oldProfileImageId = currentProfile.profile_image_idstr
        split = re.split('(\d.*)', oldProfileImageId)
        newnum = int(split[1]) + 1
        return username + str(newnum)

    if new_image:
        currentProfile.profile_image_idstr = getPotentialNewProfileImageIdStr()
        currentProfile.save()

    if pk != None:
        ckrtfholder = get_object_or_404(CKRichTextHolder, pk=pk)
        content = ckrtfholder.content
        currentProfile.about_me = content
        currentProfile.save()
    else:
        pass

    if field_to_edit != "nofield":
        content = getattr(currentProfile, field_to_edit)
        ckrtfholder = CKRichTextHolder.objects.create(author=user, field_to_edit=field_to_edit, content=content)
        pk = ckrtfholder.pk
        query_string = "/" + str(pk)
        return redirect("/ckrichtextedit" + query_string)

    context = {"profile": currentProfile, "edit": edit, "potentialNewProfileImageIdStr": getPotentialNewProfileImageIdStr()}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


### Work Utilities

@csrf_exempt
def ckrichtextedit(request, pk, template="josmembers/ckrichtextedit.html", extra_context=None):

    instance = get_object_or_404(CKRichTextHolder, pk=pk)
    form = CKRichTextEditForm(instance=instance)

    if request.method == 'POST':
        content = request.POST['content']
        instance.content = content
        instance.save()
        query_string = "/?pk=" + pk

        return redirect("/users/"+ str(instance.author_id) + query_string)

    context = {'form': form}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def personaldesk(request, pk, template="josmembers/jospersonaldesk.html", extra_context=None):
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
def members_list(request, template="josmembers/josmembers_members_list.html", extra_context=None):

    profiles = JOSProfile.objects.all()
    context = {"profiles": profiles}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


def submit_member_search_from_ajax(request):
    """
    Processes a search request
    """

    member_search_text = ""  # Assume no search

    if (request.method == "GET"):
        """
        The search form has been submitted. Get the search text - must be GET.
        """
        member_search_text = request.GET.get("member_search_t"
                                             "ext", "").strip().lower()

    member_search_results = []

    if (member_search_text != ""):
        member_search_results = JOSProfile.objects.filter(user__username__contains=member_search_text).order_by('user__username')

    # print('search_text="' + search_text + '", results=' + str(color_results))
    # Add items to the context:

    # The search text for display and result set
    context = {
        "member_search_text": member_search_text,
        "member_search_results": member_search_results
    }

    return render_to_response("josmembers/member_search_results__html_snippet.txt", context)


