from django.shortcuts import render, get_object_or_404


from josmembers.models import JOSUserCreatedNote, JOSProfile
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import JOSHelpItem

### CHANGE TO SUIT HELP SYSTEM

def help_sys(request):
    help_items = JOSHelpItem.objects.all

    user_id = request.user.id

    user = User.objects.get(id = user_id)


    profile = JOSProfile.objects.get(user=user)

    user_created_note, created = JOSUserCreatedNote.objects.get_or_create(profile = profile)

    text = user_created_note.note_text

    return {
        'help_items': help_items,
        'user_created_note': text
    }
