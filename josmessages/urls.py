from django.conf.urls import url
from django.views.generic import RedirectView

from josmessages.views import inbox, outbox, jos_message_compose, view, delete

# messages implemented to avoid disclosing addresses

urlpatterns = [
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox/'), name='messages_redirect'),
    url(r'^inbox/$', inbox, name='messages_inbox'),
    url(r'^outbox/$', outbox, name='messages_outbox'),
    url(r'^compose/(?P<id>\d+)/$', jos_message_compose, name='messages_compose'),
    url(r'^compose/*$', jos_message_compose, name='messages_compose'),
    url(r'^view/(?P<message_thread_id>[\d]+)/$', view, name='messages_detail'),
    url(r'^delete/(?P<message_thread_id>[\d]+)/$', delete, name='messages_delete'),

    # url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
    # url(r'^trash/$', trash, name='messages_trash'),
]
