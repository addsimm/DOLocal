from django.shortcuts import render, get_object_or_404

from josmembers.models import JOSUserCreatedNote, JOSProfile

from .models import JOSHelpItem

### CHANGE TO SUIT HELP SYSTEM

def help_sys(request):
    help_items = JOSHelpItem.objects.all
    from josmembers.models import JOSUserCreatedNote, JOSProfile
    try:
        profile = get_object_or_404(JOSProfile, user=request.user)
    except:
        profile = None

    if profile != None:
        try:
            user_created_note = get_object_or_404(JOSUserCreatedNote, profile = profile)
        except:
            user_created_note = JOSUserCreatedNote.objects.create(profile = profile)

        text = user_created_note.note_text

    else:
        text= ' '


    return {
        'help_items': help_items,
        'user_created_note': text
    }
