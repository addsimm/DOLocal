### josmembers/views.py
from __future__ import unicode_literals


from django.contrib.messages import info, error
from django.contrib.auth import (login as auth_login, logout as auth_logout, authenticate, get_user_model)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import activate

from mezzanine.accounts.forms import PasswordResetForm, LoginForm
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import next_url

from friendship.exceptions import AlreadyExistsError
from friendship.models import Follow

from josprojects.models import CKRichTextHolder
from .models import JOSProfile
from .forms import JOSSignupForm, JOSNewPasswordForm, JOSReserveSpaceForm

User = get_user_model()

### Login & Passwords:

def login(request, template="accounts/account_login.html",
          form_class=LoginForm, extra_context=None):
        """
        Login form.
        """
        activate('America/Los_Angeles')

        form = form_class(request.POST or None)
        if request.method == "POST" and form.is_valid():
            authenticated_user = form.save()
            info(request, _("Successfully logged in!"))
            auth_login(request, authenticated_user)
            pk = str(authenticated_user.id)
            return redirect("/josprojects/personaldesk/" + pk)

        context = {"form": form, "title": _("Log in")}
        context.update(extra_context or {})
        return TemplateResponse(request, template, context)


def logout(request):
    """
    Log the user out.
    """
    auth_logout(request)
    info(request, _("Successfully logged out - come back soon!"))
    return redirect("/")


@login_required
def account_redirect(request):
    """
    Just gives the URL prefix for accounts an action - redirect to the profile update form.
    """
    return redirect("profile_update")


def password_reset(request, template="accounts/account_password_reset.html", form_class=PasswordResetForm,
                   extra_context=None):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        send_verification_mail(request, user, "password_reset_verify")
        info(request, _("Email with password reset link sent."))
    context = {"form": form, "title": _("Reset Password")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


def password_reset_verify(request, uidb36=None, token=None):
    user = authenticate(uidb36=uidb36, token=token, is_active=True)

    if user is not None:
        auth_login(request, user)
        return redirect('jos_new_password')

    else:
        error(request, _("Sorry, the link has expired. Please enter your email address again"))
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
            info(request, _("Password changed, please login to confirm."))
            return redirect("login")

    context = {"form": form, "title": _("Reset password")}
    return TemplateResponse(request, template, context)


### Members

@login_required
def members_list(request, template="josmembers/josmembers_members_list.html", extra_context=None):
    # check request for favoring
    follow_unfollow(request)

    # List of who this user is following
    following = Follow.objects.following(request.user)

    profiles = JOSProfile.objects.all()
    context = {"profiles":  profiles,
               "following": following
               }
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
        member_search_text = request.GET.get("member_search_text", "").strip().lower()

    member_search_results = []

    if (member_search_text != ""):
        member_search_results = JOSProfile.objects.filter(user__username__contains=member_search_text).order_by(
            'user__username')

    # print('search_text="' + search_text + '", results=' + str(color_results))
    # Add items to the context:

    # The search text for display and result set
    context = {
        "member_search_text":    member_search_text,
        "member_search_results": member_search_results
    }

    return render_to_response("josmembers/member_search_results__html_snippet.txt", context)


def follow_unfollow(request):
    other_user_id = request.GET.get('add_favorite', " ")
    other_user = " "
    remove_user_id = request.GET.get('remove_favorite', " ")
    remove_user = " "

    if other_user_id != " ":
        try:
            other_user = User.objects.get(id=other_user_id)
            # Create request.user follows other_user relationship
            Follow.objects.add_follower(request.user, other_user)
            info(request, other_user.JOSProfile.jos_name() + " is now a favorite!")
        except ValidationError:
            info(request, "You cannot favorite yourself ...")
        except AlreadyExistsError:
            info(request, other_user.JOSProfile.jos_name() + " is already a favorite!")

    if remove_user_id != " ":
        try:
            remove_user = User.objects.get(id=remove_user_id)
            return_variable = Follow.objects.remove_follower(request.user, remove_user)
            if return_variable:
                info(request, remove_user.JOSProfile.jos_name() + " is no longer a favorite.")
            else:
                info(request, "Sorry, problem removing favorite - please contact us.")
        except:
            pass

        return


### Profiles:

@login_required
def josprofile_redirect(request):
    """
    Just gives the URL prefix for profiles an action - redirect
    to the logged in user's profile.
    """
    return redirect("profile", username=request.user.username)


@csrf_exempt
def josprofile(request, userid, edit, template="josmembers/josmembers_josprofile.html", extra_context=None):

    # check request for favoring
    follow_unfollow(request)

    activate('America/Los_Angeles')

    user = User.objects.get(id=userid)
    username = user.username
    currentProfile = get_object_or_404(JOSProfile, user=user)

    is_follower = False
    if request.user != user:
        is_follower = Follow.objects.follows(request.user, user)

    def getPotentialNewProfileImageIdStr():
        import re
        oldProfileImageId = currentProfile.profile_image_id_str
        split = re.split('(\d.*)', oldProfileImageId)
        newnum = int(split[1]) + 1
        return username + str(newnum)

    new_image = request.GET.get('new_image', False)
    if new_image:
        currentProfile.profile_image_id_str = getPotentialNewProfileImageIdStr()
        currentProfile.save()

    if request.method == 'POST':
        nucontent = request.POST['nucontent']
        field_to_edit = request.POST['field_to_edit']

        ckrtfholder = CKRichTextHolder.objects.create(
            author=request.user,
            parent_class='JOSStory',
            parent_id=currentProfile.id,
            field_edited=field_to_edit,
            content=getattr(currentProfile, field_to_edit)
        )

        ckrtfholder.save()

        setattr(currentProfile, field_to_edit, nucontent)
        info(request, "Changes saved!")
        currentProfile.save()

        edit = False

    context = {"profile": currentProfile,
               "edit": edit,
               "potentialNewProfileImageIdStr": getPotentialNewProfileImageIdStr(),
               "requesterfollows": is_follower}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


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
            info(request, _("Successfully signed up - this is your personal desk:"))
            auth_login(request, new_user)
            return redirect("http://www.joinourstory.com/personaldesk/" + str(new_user.id))

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
        info(request, _("Successfully signed up - this is your personal desk:"))
        return redirect("http://www.joinourstory.com/personaldesk/" + str(user.id))
    else:
        error(request, _("The link you clicked is no longer valid."))
        return redirect("/")


def reserve_space(request, template="accounts/account_reserve_space.html", extra_context=None):
    """
    Signup form.
    """
    remote_address = request.META.get('HTTP_X_REAL_IP')
    ### CHANGE ----------------------------
    signup_form = JOSReserveSpaceForm
    form = signup_form(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        reservation = form.save()

        if reservation:
            ### send_approve_mail(request, new_user)
            info(request, _("Success! We will contact you soon."))
        else:
            info(request, _("Sorry, please try again or contact us at (213) 465-0885."))

        return redirect(next_url(request) or "/")

    context = {"form": form, "title": _("Reserve place")}
    context.update({"remote_address": remote_address})
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)