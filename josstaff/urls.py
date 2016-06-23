from django.conf.urls import patterns, include, url

from mezzanine.conf import settings

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = patterns('',

   url("about/$", "josstaff.views.staffgallery", name="staffgallery"),
   url("legals/$", "josstaff.views.legals", name="legals"),
   url("community-rules/$", "josstaff.views.community_rules", name="community_rules"),

   url("^%s%s$" % ("josstaff/staff_base".strip("/"), _slash), "josstaff.views.staff_base",
       name="staff_base"),
   url("^%s%s$" % ("josstaff/referral".strip("/"), _slash), "josstaff.views.referral",
       name="referral"),
   url("^%s%s$" % ("josstaff/stafftimesheet".strip("/"), _slash), "josstaff.views.stafftimesheet",
      name="josstaff_timesheet"),
   url("^%s%s$" % ("josanal".strip("/"), _slash), "josstaff.views.josanal", name="josanal"),

)
