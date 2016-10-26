
### CHANGE TO SUIT HELP SYSTEM

def help_sys(request):
    session_key = request.session.session_key

    try:
        help_position = request.session["help_position"]
    except:
        help_position = request.session["help_position"] = 'initial'

    return {
        'session_key': session_key,
        'help_position': help_position
    }
