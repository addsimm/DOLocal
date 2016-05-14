from django.conf.urls import patterns, include, url

from .views import ckrichtextedit, personaldesk, mystory, mystory_list

from mezzanine.conf import settings

urlpatterns = patterns('',

   url("ckrichtextedit/(?P<pk>\d+)$", "josprojects.views.ckrichtextedit", name="ckrichtextedit"),
   url("ckrichtextedit", "josprojects.views.ckrichtextedit", {'pk': None}, name="ckrichtextedit"),

   url("personaldesk/(?P<pk>\d+)$", personaldesk, name="personaldesk"),
   url("personaldesk", personaldesk, {'pk': None}, name="personaldesk"),

   url("mystory_list$", mystory_list, name="mystory_list"),

   url("mystory/(?P<pk>\d+)$", mystory, name="mystory"),
   url("mystory", mystory, {'pk': 0}, name="mystory"),


)