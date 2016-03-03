from django.shortcuts import render
from josstaff.models import JOSStaffMember

# Create your views here.


def staffgallery(request):
    templates = []
    templates.append(u"josstaff/staffgallery.html")
    staff = JOSStaffMember.objects.all()
    context = {'staff': staff}
    return render(request, templates, context)