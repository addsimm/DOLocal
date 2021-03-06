from django.conf.urls import url
from .views import *

urlpatterns = [



    url("seven_day", seven_day, name="seven_day"),

    url("one_day/(?P<day_num>\d{1,3})", one_day, name="one_day"),

    url("courseweek$", course_week, name="course_week"),
    url("courseweek/(?P<week_no>\d{1,3})/(?P<part_no>\d{1,3})/(?P<segment_no>\d{1,3})/(?P<handout_id>\d{1,4})/$",
        course_week,
        name="course_week"),

    url("josstory/(?P<story_id>\d+)/*$", josstory, name="josstory"),
    url("josstory/*$", josstory, {'story_id': 0}, name="josstory"),

    url("story_update/*$", ajax_story_update, name="story_update"),

    url("story_reader/(?P<story_id>\d+)/*$", story_reader, name="story_reader"),

    url("wheel/(?P<wheel_id>\d+)/*$", joswheel, name="joswheel"),
    url("wheel/*$", joswheel, name="joswheel"),

    url("wheel_update/*$", ajax_wheel_update, name="wheel_update"),

    url("plot_template/(?P<wheel_id>\d+)/edit$", sw_plot, {'edit': True}, name="sw_plot_edit"),
    url("plot_template/(?P<wheel_id>\d+)$", sw_plot, {'edit': False}, name="sw_plot"),

    url("theme_template/(?P<wheel_id>\d+)/edit$", sw_theme, {'edit': True}, name="sw_theme_edit"),
    url("theme_template/(?P<wheel_id>\d+)$", sw_theme, {'edit': False}, name="sw_theme"),

    url("world_template/(?P<wheel_id>\d+)/edit$", sw_world, {'edit': True}, name="sw_world_edit"),
    url("world_template/(?P<wheel_id>\d+)$", sw_world, {'edit': False}, name="sw_world"),

    url("conflict_template/(?P<wheel_id>\d+)/edit$", sw_conflict, {'edit': True}, name="sw_conflict_edit"),
    url("conflict_template/(?P<wheel_id>\d+)$", sw_conflict, {'edit': False}, name="sw_conflict"),

    url("characters_template/(?P<wheel_id>\d+)/(?P<character_id>\d+)/edit$", sw_characters, {'edit': True},
        name="sw_characters_edit"),
    url("characters_template/(?P<wheel_id>\d+)/(?P<character_id>\d+)$", sw_characters, {'edit': False},
        name="sw_characters"),
    url("characters_template/(?P<wheel_id>\d+)$", sw_characters, {'edit': False},
        name="sw_characters"),

]
