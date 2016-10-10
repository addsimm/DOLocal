from django.conf.urls import patterns, include, url
from .views import course_week, course_week_list, handout, next_handout

urlpatterns = patterns('',

   url("courseweeklist", course_week_list, name="course_week_list"),

   url("courseweek/(?P<week_no>\d+)/part1", course_week, {'part': 'part1'}, name="course_week"),
   url("courseweek/(?P<week_no>\d+)/part2", course_week, {'part': 'part2'}, name="course_week"),
   url("courseweek$", course_week, name="course_week"),

   url("next_handout/*$", next_handout, name="next_handout"),

   url("handout/(?P<handout_id>\d+)/edit/*$", handout, {'edit': True}, name="handout_edit"),
   url("handout/(?P<handout_id>\d+)/*$", handout, {'edit': False}, name="handout"),
   url("handout/*$", handout, {'handout_id': 0, 'edit': False}, name="handout"),

)