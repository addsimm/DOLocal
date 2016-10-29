
from .models import JOSHelpItem

### CHANGE TO SUIT HELP SYSTEM

def help_sys(request):
    help_items = JOSHelpItem.objects.all

    return {
        'help_items': help_items
    }
