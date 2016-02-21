from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from mezzanine.accounts import views

ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
PROFILE_URL = getattr(settings, "PROFILE_URL", "/users/")
PROFILE_UPDATE_URL = getattr(settings, "PROFILE_UPDATE_URL",
                             "/%s/update/" % ACCOUNT_URL.strip("/"))

_slash = "/" if settings.APPEND_SLASH else ""

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns("",
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    ("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += patterns('',
        url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
    )

urlpatterns += patterns('',
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE

    url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),


    # HOMEPAGE FOR A BLOG-ONLY SITE

    # MEZZANINE'S URLS
    # ----------------
    # ADD YOUR OWN URLPATTERNS *ABOVE* THE LINE BELOW.
    # ``mezzanine.urls`` INCLUDES A *CATCH ALL* PATTERN
    # FOR PAGES, SO URLPATTERNS ADDED BELOW ``mezzanine.urls``
    # WILL NEVER BE MATCHED!

    # If you'd like more granular control over the patterns:

    ### JOS Staff
    url("about/$", "josstaff.views.staffgallery", name="staffgallery"),

    ### JOS Accounts
    ### url("^%s%s$" % (PROFILE_URL.strip("/"), _slash),
    ###     views.profile_redirect, name="profile_redirect"),

    url("^%s%s$" % (PROFILE_URL.strip("/"), _slash),
        "josmembers.views.josprofile_redirect", name="josprofile_redirect"),
    url("^%s/(?P<username>.*)%s$" % (PROFILE_URL.strip("/"), _slash),
        "josmembers.views.josprofile", name="josprofile"),
    url("^%s%s$" % (PROFILE_UPDATE_URL.strip("/"), _slash),
        "josmembers.views.josprofile_update", name="josprofile_update"),

    url(r'^upload/complete$', "josmembers.views.direct_upload_complete", name="direct_upload_complete"),

    ("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
