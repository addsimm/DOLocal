from django.conf.urls import patterns, include, url

from .views import ckrichtextedit, personaldesk, josstory, mystory_list, story_gallery

from mezzanine.conf import settings

urlpatterns = patterns('',

   url("ckrichtextedit/(?P<pk>\d+)$", "josprojects.views.ckrichtextedit", name="ckrichtextedit"),
   url("ckrichtextedit", "josprojects.views.ckrichtextedit", {'pk': None}, name="ckrichtextedit"),

   url("personaldesk/(?P<pk>\d+)$", personaldesk, name="personaldesk"),
   url("personaldesk", personaldesk, {'pk': None}, name="personaldesk"),

   url("mystory_list", mystory_list, name="mystory_list"),

   url("josstory/(?P<storyid>\d+)/edit/*$", josstory, {'edit': True}, name="josstory_edit"),
   url("josstory/(?P<storyid>\d+)/*$", josstory, {'edit': False}, name="josstory"),
   url("josstory/*$", josstory, {'storyid': 0, 'edit': False}, name="josstory"),

   url("story_gallery", story_gallery, name="story_gallery"),

)