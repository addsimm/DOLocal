from django.conf.urls import patterns, include, url
from .views import course_week, course_week_list, handout

urlpatterns = patterns('',

   url("courseweeklist", course_week_list, name="course_week_list"),

   url("courseweek/(?P<weekid>\d+)/$", course_week, name="course_week"),
   url("courseweek$", course_week, name="course_week"),

   url("handout/(?P<handoutid>\d+)$", handout, name="handout"),
   url("handout$", handout, name="handout"),

)