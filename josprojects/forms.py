
from django import forms

from mezzanine.core.forms import Html5Mixin

from .models import CKRichTextHolder, JOSStory

class CKRichTextEditForm(Html5Mixin, forms.ModelForm):

    pk = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model  = CKRichTextHolder
        fields = ("content", "author", 'title', 'nextURL', 'field_to_edit')
        widgets = {'author': forms.HiddenInput(),
                   'title': forms.HiddenInput(),
                   'field_to_edit': forms.HiddenInput(),
                   'nextURL': forms.HiddenInput()}
