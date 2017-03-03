from django.conf.urls import url

from mezzanine.conf import settings

from views import staff_base, staffgallery, legals, community_rules, referral, stafftimesheet, josanal

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [

    url("about/$", staffgallery, name="staffgallery"),
    url("legals/$", legals, name="legals"),
    url("community-rules/$", community_rules, name="community_rules"),

    url("^%s%s$" % ("josstaff/staff_base".strip("/"), _slash), staff_base,
        name="staff_base"),
    url("^%s%s$" % ("josstaff/referral".strip("/"), _slash), referral,
        name="referral"),
    url("^%s%s$" % ("josstaff/stafftimesheet".strip("/"), _slash), stafftimesheet,
        name="josstaff_timesheet"),
    url("^%s%s$" % ("josanal".strip("/"), _slash), josanal, name="josanal"),

]
