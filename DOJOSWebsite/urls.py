from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.conf import settings

from josprojects.views import help_update, ajax_help_search, workshop_connect, community_room
from josplayground.views import playground_view

_slash = "/" if settings.APPEND_SLASH else ""
_verify_pattern = "/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)"

ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
PASSWORD_RESET_VERIFY_URL = \
    getattr(settings, "PASSWORD_RESET_VERIFY_URL", "/%s/password/verify/" % ACCOUNT_URL.strip("/"))
JOS_NEW_PASSWORD_URL = \
    getattr(settings, "PASSWORD_RESET_VERIFY_URL", "/%s/jos_new_password/" % ACCOUNT_URL.strip("/"))

admin.autodiscover()

urlpatterns = i18n_patterns("",
    ### Admin
    ("^admin/", include(admin.site.urls)),
)

urlpatterns += patterns('',

    ### HOMEPAGE
    url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

    ### Password reset
    url("^%s%s$" % (JOS_NEW_PASSWORD_URL.strip("/"), _slash), "josmembers.views.jos_new_password",
        name="jos_new_password"),
    url("^%s%s%s$" % (PASSWORD_RESET_VERIFY_URL.strip("/"), _verify_pattern, _slash),
        "josmembers.views.password_reset_verify", name="password_reset_verify"),
    ('^', include('josmembers.urls', namespace='josmembers')),

    ##### Adam's test playground
    url("playground", playground_view, name="playground"),

    ### Tracking ###
    url(r'^tracking/', include('tracking.urls')),

    ### Help w/ search
    url("help_update", help_update, name="help_update"),
    url(r"^search_help/$", ajax_help_search, name="search_help"),

    ### Video conference ###
    url("workshop_connect$", workshop_connect, name="workshop_connect"),
    url("community_room/incognito/$", community_room, {'incognito': True}, name="community_room"),
    url("community_room/(?P<jos_id>\d+)", community_room, name="community_room"),

    ### Messages
    url(r'^messages/',
        include('josmessages.urls', namespace='josmessages', app_name='josmessages')),

    ### JOS app includes
    ("^", include("josstaff.urls", namespace='josstaff')),
    ("^", include("josprojects.urls")),
    ("^joscourses/", include("joscourses.urls", namespace='joscourses')),

    ### NOT IMPLEMENTED:
    # url(r'^spirit/', include(spirit.urls)),
    # url(r'^spirit/', include('spirit.urls', namespace="spirit", app_name='spirit')),
    # url(r'^calendar/', include('schedule.urls')),

    ##### PLACE URls *ABOVE* MEZZANINE
    ("^", include("mezzanine.urls")),
)

### DJANGO-DEBUG-TOOLBAR
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        )



### Adds 'STATIC_URL' to error page's context, so they use JS, CSS and images.
# handler404 = "mezzanine.core.views.page_not_found"
# handler500 = "mezzanine.core.views.server_error"
