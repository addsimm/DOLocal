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
            'period_date_start': forms.TextInput(attrs={'type': 'date'}),
            'period_date_end': forms.DateInput()
        }

    membertest = forms.CharField(label="Member", widget=forms.TextInput(), initial='z')
    date_field = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(JOSStaffHoursEntryForm, self).__init__(*args, **kwargs)
        self.fields['membertest'].value = 'adam'



