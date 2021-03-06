from django.conf.urls import url

from .views import personaldesk, mystory_list, story_gallery

urlpatterns = [

   # url("ckrichtextedit/(?P<pk>\d+)$", "josprojects.views.ckrichtextedit", name="ckrichtextedit"),
   # url("ckrichtextedit", "josprojects.views.ckrichtextedit", {'pk': None}, name="ckrichtextedit"),

   url("personaldesk/(?P<pk>\d+)$", personaldesk, name="personaldesk"),
   url("personaldesk", personaldesk, {'pk': None}, name="personaldesk"),

   url("mystory_list", mystory_list, name="mystory_list"),

   url("story_gallery", story_gallery, name="story_gallery"),

   # url("josstory/(?P<story_id>\d+)/edit/*$", josstory, {'edit': True}, name="josstory_edit"),
   # url("josstory/(?P<story_id>\d+)/*$", josstory, {'edit': False}, name="josstory"),
   # url("josstory/*$", josstory, {'story_id': 0, 'edit': False}, name="josstory"),
   #
   # url("story_update/*$", ajax_story_update, name="story_update"),

]