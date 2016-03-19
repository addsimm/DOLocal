from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from mezzanine.accounts import views

ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
SIGNUP_URL = getattr(settings, "SIGNUP_URL",
                     "/%s/signup/" % ACCOUNT_URL.strip("/"))
SIGNUP_VERIFY_URL = getattr(settings, "SIGNUP_VERIFY_URL",
                            "/%s/verify/" % ACCOUNT_URL.strip("/"))

PROFILE_URL = getattr(settings, "PROFILE_URL", "/users/")
PROFILE_UPDATE_URL = getattr(settings, "PROFILE_UPDATE_URL",
                             "/%s/update/" % ACCOUNT_URL.strip("/"))

PASSWORD_RESET_URL = getattr(settings, "PASSWORD_RESET_URL",
                             "/%s/password/reset/" % ACCOUNT_URL.strip("/"))

PASSWORD_RESET_VERIFY_URL = getattr(settings, "PASSWORD_RESET_VERIFY_URL",
                                    "/%s/password/verify/" % ACCOUNT_URL.strip("/"))

JOS_NEW_PASSWORD_URL = getattr(settings, "PASSWORD_RESET_VERIFY_URL",
                               "/%s/jos_new_password/" % ACCOUNT_URL.strip("/"))

LOGOUT_URL = settings.LOGOUT_URL

_verify_pattern = "/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)"
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
    # URLPATTERNS ADDED BELOW ``mezzanine.urls`` WILL NEVER BE MATCHED!

    ### JOS Staff

    url("about/$", "josstaff.views.staffgallery", name="staffgallery"),

    ### JOS Accounts & Members ###

    url("^%s%s$" % (LOGOUT_URL.strip("/"), _slash),
        "josmembers.views.logout", name="logout"),

    url("^%s%s$" % (SIGNUP_URL.strip("/"), _slash),
        "josmembers.views.signup", name="signup"),
    url("^%s%s%s$" % (SIGNUP_VERIFY_URL.strip("/"), _verify_pattern, _slash),
        "josmembers.views.signup_verify", name="signup_verify"),

    url("^%s%s$" % (PASSWORD_RESET_URL.strip("/"), _slash),
        "josmembers.views.password_reset", name="jos_password_reset"),
    url("^%s%s$" % (JOS_NEW_PASSWORD_URL.strip("/"), _slash),
        "josmembers.views.jos_new_password", name="jos_new_password"),
    url("^%s%s%s$" %
        (PASSWORD_RESET_VERIFY_URL.strip("/"), _verify_pattern, _slash),
        "josmembers.views.password_reset_verify", name="password_reset_verify"),

    url("^%s%s$" % ("josstaff/stafftimesheet".strip("/"), _slash),
        "josstaff.views.stafftimesheet", name="josstaff_timesheet"),


    url("^%s/(?P<username>.*)%s$" % (PROFILE_URL.strip("/"), _slash),
        "josmembers.views.josprofile", name="josprofile"),



    url("^%s%s$" % (PROFILE_URL.strip("/"), _slash),
        "josmembers.views.josprofile_redirect", name="josprofile_redirect"),
    url("^%s%s$" % (PROFILE_UPDATE_URL.strip("/"), _slash),
        "josmembers.views.josprofile_update", name="josprofile_update"),


    ### DJOINGO ###

    url("djoingo/$", "josdjoingo.views.djoingo_main", name="djoingo_main"),

    ###############

    ("^", include("mezzanine.urls")),

    # MOUNTING MEZZANINE UNDER A PREFIX
    # ---------------------------------
    # ("^%s/" % settings.SITE_PREFIX, include("mezzanine.urls"))

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
