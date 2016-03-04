from django.shortcuts import render
from django.template.response import TemplateResponse

# Create your views here.


def djoingo_main(request):
    """
    Main Djoingo View
    """
    template = "josdjoingo/djoingo_main.html"
    context = {}

    return TemplateResponse(request, template, context)


