from django.conf.urls import patterns, include, url
from .views import course_week, course_week_list

urlpatterns = patterns('',

   url("courseweeklist", course_week_list, name="course_week_list"),

   url("courseweek/(?P<weekid>\d+)/edit/*$", course_week, {'edit': True}, name="course_week_edit"),
   url("courseweek/(?P<weekid>\d+)/*$", course_week, {'edit': False}, name="course_week"),
   url("courseweek/*$", course_week, {'storyid': 0, 'edit': False}, name="course_week"),

)