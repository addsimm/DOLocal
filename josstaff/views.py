from django.shortcuts import render

# Create your views here.


def staffgallery(request):
    templates = []
    templates.append(u"josstaff/staffgallery.html")
    context = {}
    return render(request, templates, context)