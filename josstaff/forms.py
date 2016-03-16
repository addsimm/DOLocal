from django import forms

from mezzanine.core.forms import Html5Mixin

from .models import JOSStaffHoursEntry


class JOSStaffHoursEntryForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for JOSStaffHoursEntry.
    """

    class Meta:
        model = JOSStaffHoursEntry
        fields = '__all__'
        widgets = {
            'staff_member': forms.HiddenInput(),
            'time_claim_approved': forms.HiddenInput(),
            'period_date_start': forms.DateInput(),
            'period_date_end': forms.DateInput()
        }


    def __init__(self, *args, **kwargs):
        super(JOSStaffHoursEntryForm, self).__init__(*args, **kwargs)




