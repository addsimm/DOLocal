
from django.conf.urls import include, url
from django.contrib import admin

from mezzanine.conf import settings
from mezzanine.pages.views import page

from josmembers.views import jos_new_password, password_reset_verify
from josprojects.views import ajax_session_update, ajax_help_search, workshop_connect, community_room
from josplayground.views import playground_view, ui_demo_view

_slash = "/" if settings.APPEND_SLASH else ""
_verify_pattern = "/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)"

ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
PASSWORD_RESET_VERIFY_URL = \
    getattr(settings, "PASSWORD_RESET_VERIFY_URL", "/%s/password/verify/" % ACCOUNT_URL.strip("/"))
JOS_NEW_PASSWORD_URL = \
    getattr(settings, "PASSWORD_RESET_VERIFY_URL", "/%s/jos_new_password/" % ACCOUNT_URL.strip("/"))

admin.autodiscover()

urlpatterns = [
    ### Admin
    url("^admin/", include(admin.site.urls)),
]

urlpatterns += [

    ### HOMEPAGE
    url("^$", page, {"slug": "/"}, name="home"),

    ### Password reset
    url("^%s%s$" % (JOS_NEW_PASSWORD_URL.strip("/"), _slash), jos_new_password,
        name="jos_new_password"),
    url("^%s%s%s$" % (PASSWORD_RESET_VERIFY_URL.strip("/"), _verify_pattern, _slash),
        password_reset_verify, name="password_reset_verify"),
    url('^', include('josmembers.urls', namespace='josmembers')),

    ##### Adam's test playground
    url("playground", playground_view, name="playground"),
    url("uidemo", ui_demo_view, name="ui_demo"),

    ### Tracking ###
    # url(r'^tracking/', include('tracking.urls')),

    ### Help w/ search
    url("ajax_session_update", ajax_session_update, name="ajax_session_update"),
    url(r"^search_help/$", ajax_help_search, name="search_help"),

    ### Video conference ###
    url("workshop_connect$", workshop_connect, name="workshop_connect"),
    url("community_room/incognito/$", community_room, {'incognito': True}, name="community_room"),
    url("community_room/(?P<jos_id>\d+)", community_room, name="community_room"),

    ### Messages
    url(r'^messages/',
        include('josmessages.urls', namespace='josmessages', app_name='josmessages')),

    ### JOS app includes
    url("^", include("josstaff.urls", namespace='josstaff')),
    url("^", include("josprojects.urls")),
    url("^joscourses/", include("joscourses.urls", namespace='joscourses')),


    ##### PLACE URls *ABOVE* MEZZANINE
    url("^", include("mezzanine.urls")),
]

### DJANGO-DEBUG-TOOLBAR
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

### Adds 'STATIC_URL' to error page's context, so they use JS, CSS and images.
# handler404 = "mezzanine.core.views.page_not_found"
# handler500 = "mezzanine.core.views.server_error"
