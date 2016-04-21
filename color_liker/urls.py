from django.conf.urls import patterns, include, url
from color_liker.views import ColorList

urlpatterns = patterns('',

    # Used as both the main page url, and for the search-form submission.
    # If the GET object exists, then the search-form is being submitted.
    # Otherwise, it's a normal page request.
    url(r"^$", ColorList.as_view(), name="color_list"),

    url(r"^like_color_(?P<color_id>\d+)/$", "color_liker.views.toggle_color_like",
       name="toggle_color_like"),

    url(r"^search/$", "color_liker.views.submit_color_search_from_ajax", name="search_color_list"),

)