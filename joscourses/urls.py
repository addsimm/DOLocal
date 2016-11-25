from django.conf.urls import patterns, include, url
from .views import course_week, course_week_list, storywheel, sw_plot # next_handout

urlpatterns = patterns(
        '',

    url("courseweeklist", course_week_list, name="course_week_list"),

    url("courseweek/(?P<week_no>\d{1,3})/(?P<part_no>\d{1,3})/(?P<segment_no>\d{1,3})/(?P<handout_id>\d{1,4})/$", course_week,
       name="course_week"),

    url("courseweek$", course_week, name="course_week"),


    url("storywheel", storywheel, name="storywheel"),

    url("sw_plot", sw_plot, name="sw_plot"),
)

