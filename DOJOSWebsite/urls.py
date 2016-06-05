from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.conf import settings

_slash = "/" if settings.APPEND_SLASH else ""
_verify_pattern = "/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)"

ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
PASSWORD_RESET_VERIFY_URL = getattr(settings, "PASSWORD_RESET_VERIFY_URL",
                                    "/%s/password/verify/" % ACCOUNT_URL.strip("/"))
JOS_NEW_PASSWORD_URL = getattr(settings, "PASSWORD_RESET_VERIFY_URL", "/%s/jos_new_password/" % ACCOUNT_URL.strip("/"))

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
urlpatterns = i18n_patterns("",
    ### Admin
    ("^admin/", include(admin.site.urls)),
)

# if settings.USE_MODELTRANSLATION:
#     urlpatterns += patterns('',
#         url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
#     )

import spirit.urls

urlpatterns += patterns('',
    # EDITABLE HOMEPAGE
    url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),

    ### Analytics ###
    url(r'^tracking/', include('tracking.urls')),

    ### JOS Members / Accounts ###
    url("^%s%s$" % (JOS_NEW_PASSWORD_URL.strip("/"), _slash), "josmembers.views.jos_new_password", name="jos_new_password"),
    url("^%s%s%s$" % (PASSWORD_RESET_VERIFY_URL.strip("/"), _verify_pattern, _slash), "josmembers.views.password_reset_verify",name="password_reset_verify"),
    ('^', include('josmembers.urls')),

    ### JOS Projects / Courses ###
    ("^", include("josprojects.urls")),
    ("^joscourses/", include("joscourses.urls")),

    ### JOS Staff ###
    url("about/$", "josstaff.views.staffgallery", name="staffgallery"),
    url("legals/$", "josstaff.views.legals", name="legals"),
    url("community-rules/$", "josstaff.views.community_rules", name="community_rules"),
    url("^%s%s$" % ("josstaff/stafftimesheet".strip("/"), _slash), "josstaff.views.stafftimesheet", name="josstaff_timesheet"),
    url("^%s%s$" % ("josanal".strip("/"), _slash), "josstaff.views.josanal", name="josanal"),

    ### DJOINGO ###
    # url("djoingo/$", "josdjoingo.views.djoingo_main", name="djoingo_main"),

    ### Forums, Messaging, Etc. ###
    url(r'^spirit/', include(spirit.urls)),
    #url(r'^spirit/', include('spirit.urls', namespace="spirit", app_name='spirit')),
    # messages implemented to avoid disclosing addresses
    url(r'^messages/compose/(?P<id>\d+)/$', "josmembers.views.jos_message_compose", name='messages_compose'),
    url(r'^messages/reply/(?P<message_id>[\d]+)/$', "josmembers.views.jos_message_reply", name='messages_reply'),
    url(r'^messages/', include('josmessages.urls')),

    # NOT IMPLEMENTED url(r'^calendar/', include('schedule.urls')),

    ### ADD URLPATTERNS *ABOVE* MEZZANINE'S URLS
    ("^", include("mezzanine.urls")),
)

### DJANGO-DEBUG-TOOLBAR
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
        )

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
