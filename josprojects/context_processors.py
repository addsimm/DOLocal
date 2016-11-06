
from numbers import Number
from django.contrib.auth import get_user_model

from josmembers.models import JOSUserCreatedNote, JOSProfile
from .models import JOSHelpItem

User = get_user_model()

def help_sys(request):

    context = {}
    if isinstance(request.user.id, Number):
        help_items = JOSHelpItem.objects.all

        user = User.objects.get(id =request.user.id)


        profile = JOSProfile.objects.get(user=user)

        user_created_note, created = JOSUserCreatedNote.objects.get_or_create(profile = profile)

        text = user_created_note.note_text

        context = {
            'help_items': help_items,
            'user_created_note': text
        }

    return context
