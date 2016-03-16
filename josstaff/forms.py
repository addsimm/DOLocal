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
            'period_date_start': forms.HiddenInput(attrs = {'id': 'period_start_date_field', 'required': 'true'}),
            'period_date_end': forms.HiddenInput(attrs={'id': 'period_end_date_field', 'required': 'true'})
        }


    def __init__(self, *args, **kwargs):
        super(JOSStaffHoursEntryForm, self).__init__(*args, **kwargs)




