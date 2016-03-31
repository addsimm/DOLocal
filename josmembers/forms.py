### josmembers/forms.py
from __future__ import unicode_literals

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.manager import Manager
from django import forms
from django.utils.http import int_to_base36
from django.utils.translation import ugettext, ugettext_lazy as _
from django.shortcuts import get_object_or_404, render_to_response


from mezzanine.accounts import (get_profile_model, get_profile_user_fieldname,
                                get_profile_for_user, ProfileNotConfigured)
from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin,TinyMceWidget
from mezzanine.utils.urls import slugify, unique_slug

from .models import CKRichTextHolder

User = get_user_model()

_exclude_fields = tuple(getattr(settings, "ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS", ()))

# If a profile model has been configured with the ``AUTH_PROFILE_MODULE``
# setting, create a model form for it that will have its fields added to
# ``ProfileForm``.
try:
    class ProfileFieldsForm(forms.ModelForm):
        class Meta:
            model = get_profile_model()
            exclude = (get_profile_user_fieldname(),) + _exclude_fields
except ProfileNotConfigured:
    pass

if settings.ACCOUNTS_NO_USERNAME:
    _exclude_fields += ("username",)
    username_label = _("Email address")
else:
    username_label = _("Username or email address")


class JOSProfileForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for auth.User - ``AUTH_PROFILE_MODULE``fields injected into the form.
    """

    class Meta:
        model = User
        fields = ("first_name", "last_name")
        exclude = _exclude_fields

    def __init__(self, *args, **kwargs):
        super(JOSProfileForm, self).__init__(*args, **kwargs)

        # Add any profile fields to the form.
        try:
            profile_fields_form = self.get_profile_fields_form()
            profile_fields = profile_fields_form().fields
            self.fields = profile_fields
            # self.fields.update(profile_fields)
            # if not self._signup:
            user_profile = get_profile_for_user(self.instance)
            for field in profile_fields:
                value = getattr(user_profile, field)
                # Check for multiple initial values, i.e. a m2m field
                if isinstance(value, Manager):
                    value = value.all()
                self.initial[field] = value
        except ProfileNotConfigured:
            pass

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied generates a unique username.
        """

        kwargs["commit"] = False
        user = super(JOSProfileForm, self).save(*args, **kwargs)

        try:
            profile = get_profile_for_user(user)
            profile_form = self.get_profile_fields_form()
            profile_form(self.data, self.files, instance=profile).save()
        except ProfileNotConfigured:
            pass

        return user

    def get_profile_fields_form(self):
        try:
            return ProfileFieldsForm
        except NameError:
            raise ProfileNotConfigured


class JOSSignupForm(Html5Mixin, forms.ModelForm):
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput(render_value=False))

    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        exclude = _exclude_fields

    def __init__(self, *args, **kwargs):
        super(JOSSignupForm, self).__init__(*args, **kwargs)
        self._signup = self.instance.id is None
        user_fields = set([f.name for f in User._meta.get_fields()])
        try:
            self.fields["username"].help_text = ugettext(
                "Only letters, numbers, dashes or underscores please")
        except KeyError:
            pass
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True
            # Disable auto-complete for password fields.
            # Password isn't required for profile update.
            if field.startswith("password"):
                self.fields[field].widget.attrs["autocomplete"] = "off"
                self.fields[field].widget.attrs.pop("required", "")

    def clean_username(self):
        """
        Ensure the username doesn't exist or contain invalid chars.
        We limit it to slugifiable chars since it's used as the slug
        for the user's profile view.
        """
        username = self.cleaned_data.get("username")
        if username.lower() != slugify(username).lower():
            raise forms.ValidationError(
                ugettext("Username can only contain letters, numbers, dashes "
                         "or underscores."))
        lookup = {"username__iexact": username}
        try:
            User.objects.exclude(id=self.instance.id).get(**lookup)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            ugettext("This username is already registered"))

    def clean_password2(self):
        """
        Ensure the password fields are equal, and match the minimum
        length defined by ``ACCOUNTS_MIN_PASSWORD_LENGTH``.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append(ugettext("Passwords do not match"))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                    ugettext("Password must be at least %s characters") %
                    settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.exclude(id=self.instance.id).filter(email=email)
        if len(qs) == 0:
            return email
        raise forms.ValidationError(
            ugettext("This email is already registered"))

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """

        kwargs["commit"] = False
        user = super(JOSSignupForm, self).save(*args, **kwargs)
        try:
            self.cleaned_data["username"]
        except KeyError:
            if not self.instance.username:
                try:
                    username = ("%(first_name)s %(last_name)s" %
                                self.cleaned_data).strip()
                except KeyError:
                    username = ""
                if not username:
                    username = self.cleaned_data["email"].split("@")[0]
                qs = User.objects.exclude(id=self.instance.id)
                user.username = unique_slug(qs, "username", slugify(username))
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        elif self._signup:
            try:
                user.set_unusable_password()
            except AttributeError:
                # This could happen if using a custom user model that
                # doesn't inherit from Django's AbstractBaseUser.
                pass
        user.save()

        if self._signup:
            if (settings.ACCOUNTS_VERIFICATION_REQUIRED or
                    settings.ACCOUNTS_APPROVAL_REQUIRED):
                user.is_active = False
                user.save()
            else:
                token = default_token_generator.make_token(user)
                user = authenticate(uidb36=int_to_base36(user.id),
                                    token=token,
                                    is_active=True)
        return user


class JOSNewPasswordForm(Html5Mixin, forms.ModelForm):

    # user_id = forms.HiddenInput()
    # fakeemail = forms.EmailField(label="Change for Account Email:")
    password1 = forms.CharField(label=_("New Password"),
                                widget=forms.PasswordInput(render_value=False))

    password2 = forms.CharField(label=_("Confirm New Password"),
                                widget=forms.PasswordInput(render_value=False))

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(JOSNewPasswordForm, self).__init__(*args, **kwargs)
        # self.user_id = self.data['user_id']
        for field in self.fields:
            if field.startswith("password"):
                self.fields[field].widget.attrs["autocomplete"] = "off"
                self.fields[field].widget.attrs.pop("required", "")
            self.fields["email"].widget.attrs["readonly"] = "readonly"

    def clean_password2(self):
        """
        Ensure the password fields are equal, and match the minimum
        length defined by ``ACCOUNTS_MIN_PASSWORD_LENGTH``.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1:
            errors = []
            if password1 != password2:
                errors.append(ugettext("Passwords do not match"))
            if len(password1) < settings.ACCOUNTS_MIN_PASSWORD_LENGTH:
                errors.append(
                    ugettext("Password must be at least %s characters") %
                    settings.ACCOUNTS_MIN_PASSWORD_LENGTH)
            if errors:
                self._errors["password1"] = self.error_class(errors)
        return password2

    def save(self, *args, **kwargs):
        """
        Create the new user. If no username is supplied (may be hidden
        via ``ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS`` or
        ``ACCOUNTS_NO_USERNAME``), we generate a unique username, so
        that if profile pages are enabled, we still have something to
        use as the profile's slug.
        """
        kwargs["commit"] = False
        user = super(JOSNewPasswordForm, self).save(*args, **kwargs)

        password = self.cleaned_data.get("password1")

        user.set_password(password)
        user.save()

        return user


class CKRichTextEditForm(Html5Mixin, forms.ModelForm):

    class Meta:
        model  = CKRichTextHolder
        fields = ("content",)
