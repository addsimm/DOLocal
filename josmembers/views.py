### josmembers/views.py
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.messages import info, error
from django.contrib.auth import (login as auth_login, logout as auth_logout, authenticate, get_user_model)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _


from mezzanine.accounts.forms import PasswordResetForm, LoginForm
from mezzanine.conf import settings
from mezzanine.utils.email import send_verification_mail, send_approve_mail
from mezzanine.utils.urls import login_redirect, next_url

from josmessages.utils import format_quote, get_username_field
from josmessages.models import Message

from friendship.exceptions import AlreadyExistsError
from friendship.models import Follow

from josprojects.models import CKRichTextHolder
from .models import JOSProfile
from .forms import JOSSignupForm, JOSNewPasswordForm, JOSComposeForm

User = get_user_model()

def login(request, template="accounts/account_login.html",
          form_class=LoginForm, extra_context=None):
        """
        Login form.
        """
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


### Profiles:

@login_required
def josprofile_redirect(request):
    """
    Just gives the URL prefix for profiles an action - redirect
    to the logged in user's profile.
    """
    return redirect("profile", username=request.user.username)


def josprofile(request, userid, edit, template="josmembers/josmembers_josprofile.html", extra_context=None):
    user = User.objects.get(id=userid)
    username = user.username
    currentProfile = get_object_or_404(JOSProfile, user=user)

    def getPotentialNewProfileImageIdStr():
        import re
        oldProfileImageId = currentProfile.profile_image_idstr
        split = re.split('(\d.*)', oldProfileImageId)
        newnum = int(split[1]) + 1
        return username + str(newnum)

    new_image = request.GET.get('new_image', False)
    if new_image:
        currentProfile.profile_image_idstr = getPotentialNewProfileImageIdStr()
        currentProfile.save()

    pk = request.GET.get('pk', None)
    if pk != None:
        ckrtfholder = get_object_or_404(CKRichTextHolder, pk=pk)
        content = ckrtfholder.content
        currentProfile.about_me = content
        currentProfile.save()
    else:
        pass

    field_to_edit = request.GET.get('field_to_edit', "nofield")
    if field_to_edit != "nofield":
        content = getattr(currentProfile, field_to_edit)

        ckrtfholder = CKRichTextHolder.objects.create(
            author=user,
            title='Profile',
            field_to_edit=field_to_edit,
            content=content)

        nexturl = '/users/' + str(user.id) + '/?pk=' + str(ckrtfholder.pk)
        ckrtfholder.nextURL = nexturl
        ckrtfholder.save()

        query_string = "/" + str(ckrtfholder.pk)

        return redirect("/ckrichtextedit" + query_string)

    context = {"profile": currentProfile,
               "edit": edit,
               "potentialNewProfileImageIdStr": getPotentialNewProfileImageIdStr()}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


### Signup & Passwords:

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


def password_reset(request, template="accounts/account_password_reset.html", form_class=PasswordResetForm, extra_context=None):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        send_verification_mail(request, user, "password_reset_verify")
        info(request, _("Email with password reset link sent."))
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
            info(request, _("Password changed, please login to confirm."))
            return redirect("login")

    context = {"form": form, "title": _("Reset password")}
    return TemplateResponse(request, template, context)


### Members

@login_required
def members_list(request, template="josmembers/josmembers_members_list.html", extra_context=None):

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
                info(request, "Sorry, problme removing favortie - please contact us.")
        except:
            pass

    # List of who this user is following
    following = Follow.objects.following(request.user)

    profiles = JOSProfile.objects.all()
    context = {"profiles": profiles,
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
        member_search_results = JOSProfile.objects.filter(user__username__contains=member_search_text).order_by('user__username')

    # print('search_text="' + search_text + '", results=' + str(color_results))
    # Add items to the context:

    # The search text for display and result set
    context = {
        "member_search_text": member_search_text,
        "member_search_results": member_search_results
    }

    return render_to_response("josmembers/member_search_results__html_snippet.txt", context)


### Messaging

@login_required
def jos_message_compose(request, id=None, form_class=JOSComposeForm,
            template_name='josmessages/compose.html', success_url=None, recipient_filter=None):
    """
    Displays and handles the ``form_class`` form to compose new messages.
    Required Arguments: None
    Optional Arguments:
        ``recipient``: username of a `django.contrib.auth` User, who should
                       receive the message, optionally multiple usernames
                       could be separated by a '+'
        ``form_class``: the form-class to use
        ``template_name``: the template to use
        ``success_url``: where to redirect after successfull submission
    """

    recipient= to_user = recipients = None

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            if 'next' in request.GET:
                success_url = request.GET['next']
            return HttpResponseRedirect(success_url)
    else:
        form = form_class()
        to_user = User.objects.get(id=id)
        if recipient is not None:
            recipients = [u for u in User.objects.filter(
                **{'%s__in' % get_username_field(): [r.strip() for r in recipient.split('+')]})]
            form.fields['recipient'].initial = recipients

    return render_to_response(template_name, {
        'form': form,
        'recipient': to_user.username,
        'jos_name': to_user.JOSProfile.jos_name,
        'id': id
    }, context_instance=RequestContext(request))


@login_required
def jos_message_reply(request, message_id, form_class=JOSComposeForm,
          template_name='josmessages/compose.html', success_url=None,
          recipient_filter=None, quote_helper=format_quote,
          subject_template=_(u"Re: %(subject)s"), ):
    """
    Prepares the ``form_class`` form for writing a reply to a given message
    (specified via ``message_id``). Uses the ``format_quote`` helper from
    ``messages.utils`` to pre-format the quote. To change the quote format
    assign a different ``quote_helper`` kwarg in your url-conf.

    """
    parent = get_object_or_404(Message, id=message_id)

    if parent.sender != request.user and parent.recipient != request.user:
        raise Http404

    if request.method == "POST":
        sender = request.user
        form = form_class(request.POST, recipient_filter=recipient_filter)
        if form.is_valid():
            form.save(sender=request.user, parent_msg=parent)
            messages.info(request, _(u"Message successfully sent."))
            if success_url is None:
                success_url = reverse('messages_inbox')
            return HttpResponseRedirect(success_url)
    else:
        form = form_class(initial={
            'body': quote_helper(parent.sender.JOSProfile.jos_name(), parent.body),
            'subject': subject_template % {'subject': parent.subject},
            'recipient': [parent.sender, ]
        })
    return render_to_response(template_name, {
        'form': form,
        'recipient': parent.sender.username,
        'jos_name': parent.sender.JOSProfile.jos_name
    }, context_instance=RequestContext(request))