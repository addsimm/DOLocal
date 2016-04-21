from django.shortcuts import redirect, render_to_response
from django.views.generic import ListView
from color_liker.models import Color

MIN_SEARCH_CHARS = 2
"""
The minimum number of characters required in a search. If there are less,
the form submission is ignored. This value is used by the below view and
the template.
"""


class ColorList(ListView):
    """
    Displays all colors in a table with only two columns: the name of the
    color, and a "like/unlike" button.
    """
    model = Color
    context_object_name = "colors"

    def dispatch(self, request, *args, **kwargs):
        self.request = request  # So get_context_data can access it.
        return super(ColorList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Returns the all colors, for display in the main table. The search
        result query set, if any, is passed as context.
        """
        return super(ColorList, self).get_queryset()

    def get_context_data(self, **kwargs):
        # The current context.
        context = super(ColorList, self).get_context_data(**kwargs)

        return context


def submit_color_search_from_ajax(request):
    """
    Processes a search request
    """

    color_search_text = ""  # Assume no search

    if (request.method == "GET"):
        """
        The search form has been submitted. Get the search text from
        it. Must be GET, not post.
        """

        color_search_text = request.GET.get("color_search_text", "").strip().lower()

    color_search_results = []

    if (color_search_text != ""):
        color_search_results = Color.objects.filter(name__contains=color_search_text)

    # print('search_text="' + search_text + '", results=' + str(color_results))


    # Add items to the context:

    # The search text for display and result set
    context = {
        "color_search_text": color_search_text,
        "color_search_results": color_search_results
    }

    return render_to_response("color_liker/color_search_results__html_snippet.txt", context)


def toggle_color_like(request, color_id):
    """Toggle "like" for a single color, then refresh the color-list page."""
    color = None
    try:
        # There's only one object with this id, but this returns a list
        # of length one. Get the first (index 0)
        color = Color.objects.filter(id=color_id)[0]
    except Color.DoesNotExist as e:
        raise ValueError("Unknown color.id=" + str(color_id) + ". Original error: " + str(e))

    # print("pre-toggle:  color_id=" + str(color_id) + ", color.is_favorited=" + str(color.is_favorited) + "")

    color.is_favorited = not color.is_favorited
    color.save()  # Commit the change to the database

    # print("post-toggle: color_id=" + str(color_id) + ", color.is_favorited=" + str(color.is_favorited) + "")

    ### return redirect("color_list")  # See urls.py

    # Render the just-clicked-on like-button.
    return render_to_response("color_liker/color_like_link__html_snippet.txt", {"color": color})

