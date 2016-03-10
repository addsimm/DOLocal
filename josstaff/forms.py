from django import forms
from django.shortcuts import get_object_or_404, render_to_response

from mezzanine.core.forms import Html5Mixin

from .models import JOSStaffHoursEntry


class JOSStaffHoursEntryForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for JOSStaffHoursEntry.
    """

    class Meta:
        model = JOSStaffHoursEntry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(JOSStaffHoursEntryForm, self).__init__(*args, **kwargs)
