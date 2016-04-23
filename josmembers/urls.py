from django.conf.urls import patterns, include, url
from color_liker.views import ColorList
from views import members_list, submit_member_search_from_ajax



urlpatterns = patterns('',

    # Used as both the main page url, and for the search-form submission.
    # If the GET object exists, then the search-form is being submitted.
    # Otherwise, it's a normal page request.

    url("josmembers_list", members_list, name="josmembers_list"),

    url(r"^search/$", submit_member_search_from_ajax, name="search_member_list"),

)