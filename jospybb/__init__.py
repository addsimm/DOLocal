from django import VERSION

if VERSION[:2] < (1, 7):
    from jospybb import signals
    signals.setup()
else:
    default_app_config = 'jospybb.apps.PybbConfig'
