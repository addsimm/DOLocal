from django.conf.urls import url
from django.views.generic import RedirectView

from josmessages.views import message_box, jos_message_compose, ajax_message_info, delete

# messages implemented to avoid disclosing addresses

urlpatterns = [
    url(r'^$', RedirectView.as_view(permanent=True, url='inbox/'), name='messages_redirect'),
    url(r'^inbox/$', message_box, name='messages_inbox'),
    url(r'^compose/(?P<id>\d+)/$', jos_message_compose, name='messages_compose'),
    url(r'^compose/*$', jos_message_compose, name='messages_compose'),


    # url(r'^view/(?P<message_thread_id>[\d]+)/$', view, name='messages_detail'),
    url(r'^delete/(?P<message_thread_id>[\d]+)/$', delete, name='messages_delete'),

    url("ajax_message_info", ajax_message_info, name="ajax_message_info")

    # url(r'^undelete/(?P<message_id>[\d]+)/$', undelete, name='messages_undelete'),
    # url(r'^trash/$', trash, name='messages_trash'),
]
