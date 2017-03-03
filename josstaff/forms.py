from django import forms

from mezzanine.core.forms import Html5Mixin

from .models import JOSStaffHoursEntry, JOSReferral


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


class JOSReferralForm(Html5Mixin, forms.ModelForm):
    """
    ModelForm for JOSReferral.
    """

    class Meta:
        model = JOSReferral

        fields = '__all__'
        widgets = {
            'staff_member': forms.HiddenInput(),
            'referral_notes': forms.Textarea()
        }

        first_name = forms.CharField(label='First')
        last_name = forms.CharField(label='Last name')
        referral_email = forms.EmailField(label='Email')
        referral_phone = forms.CharField(label='Phone')
        referral_city = forms.CharField(label='City')
        referral_notes = forms.CharField(label='Notes')

