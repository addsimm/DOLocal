from django.conf.urls import patterns, include, url
from .views import course_week, course_week_list, handout, nexthandout

urlpatterns = patterns('',

   url("courseweeklist", course_week_list, name="course_week_list"),

   url("courseweek/(?P<weekid>\d+)/$", course_week, name="course_week"),
   url("courseweek$", course_week, name="course_week"),

   url("nexthandout/*$", nexthandout, name="nexthandout"),

   url("handout/(?P<handoutid>\d+)/edit/*$", handout, {'edit': True}, name="handout_edit"),
   url("handout/(?P<handoutid>\d+)/*$", handout, {'edit': False}, name="handout"),
   url("handout/*$", handout, {'handoutid': 0, 'edit': False}, name="handout"),



)