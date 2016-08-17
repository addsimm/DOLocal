from django.conf.urls import patterns, include, url
from views import members_list, submit_member_search_from_ajax, reserve_space

from mezzanine.conf import settings

_verify_pattern = "/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)"
_slash = "/" if settings.APPEND_SLASH else ""

LOGIN_URL = settings.LOGIN_URL
LOGOUT_URL = settings.LOGOUT_URL
ACCOUNT_URL = getattr(settings, "ACCOUNT_URL", "/accounts/")
SIGNUP_URL = getattr(settings, "SIGNUP_URL", "/%s/signup/" % ACCOUNT_URL.strip("/"))
SIGNUP_VERIFY_URL = getattr(settings, "SIGNUP_VERIFY_URL", "/%s/verify/" % ACCOUNT_URL.strip("/"))
PROFILE_URL = getattr(settings, "PROFILE_URL", "/users/")
PROFILE_UPDATE_URL = getattr(settings, "PROFILE_UPDATE_URL", "/%s/update/" % ACCOUNT_URL.strip("/"))
PASSWORD_RESET_URL = getattr(settings, "PASSWORD_RESET_URL", "/%s/password/reset/" % ACCOUNT_URL.strip("/"))


urlpatterns = patterns('',

    url("^%s/(?P<userid>.*)/edit%s$" % (PROFILE_URL.strip("/"), _slash),
       "josmembers.views.josprofile", {'edit': True}, name="josprofile_edit"),
    url("^%s/(?P<userid>.*)%s$" % (PROFILE_URL.strip("/"), _slash),
       "josmembers.views.josprofile", {'edit': False}, name="josprofile"),
    url("^%s%s$" % (PROFILE_URL.strip("/"), _slash),
       "josmembers.views.josprofile_redirect", name="josprofile_redirect"),
    url("^%s%s$" % (LOGIN_URL.strip("/"), _slash),
       "josmembers.views.login", name="login"),
    url("^%s%s$" % (LOGOUT_URL.strip("/"), _slash),
       "josmembers.views.logout", name="logout"),
    url("^%s%s$" % (SIGNUP_URL.strip("/"), _slash),
       "josmembers.views.signup", name="jossignup"),
    url("^%s%s%s$" % (SIGNUP_VERIFY_URL.strip("/"), _verify_pattern, _slash),
       "josmembers.views.signup_verify", name="signup_verify"),
    url("^%s%s$" % (PASSWORD_RESET_URL.strip("/"), _slash),
       "josmembers.views.password_reset", name="jos_password_reset"),

    url("reserve_space", reserve_space, name="josreservespace"),

   # friends AJAX search

    url("josmembers_list", members_list, name="josmembers_list"),
    url(r"^search/$", submit_member_search_from_ajax, name="search_member_list"),

)