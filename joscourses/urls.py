from django.conf.urls import patterns, url
from .views import course_week, course_week_list, josstory, ajax_story_update, ajax_storywheel_update, storywheel, sw_plot

urlpatterns = patterns(
        '',

    url("courseweek$", course_week, name="course_week"),

    url("courseweeklist", course_week_list, name="course_week_list"),

    url("courseweek/(?P<week_no>\d{1,3})/(?P<part_no>\d{1,3})/(?P<segment_no>\d{1,3})/(?P<handout_id>\d{1,4})/$", course_week,
       name="course_week"),

    url("josstory/(?P<story_id>\d+)/edit/*$", josstory, {'edit': True}, name="josstory_edit"),
    url("josstory/(?P<story_id>\d+)/*$", josstory, {'edit': False}, name="josstory"),
    url("josstory/*$", josstory, {'story_id': 0, 'edit': False}, name="josstory"),

    url("story_update/*$", ajax_story_update, name="story_update"),

    url("storywheel/(?P<wheel_id>\d+)/*$", storywheel, name="storywheel"),
    url("storywheel/*$", storywheel, name="storywheel"),

    url("storywheel_update/*$", ajax_storywheel_update, name="storywheel_update"),

    url("plot_template/(?P<wheel_id>\d+)/edit$", sw_plot, {'edit': True}, name="sw_plot_edit"),
    url("plot_template/(?P<wheel_id>\d+)$", sw_plot, {'edit': False}, name="sw_plot"),

)

