

from django.shortcuts import render, get_object_or_404
from josstaff.models import JOSStaffMember

# Create your views here.


def staffgallery(request, template="josstaff/staffgallery.html", extra_context= None):
    staff = JOSStaffMember.objects.all()
    context = {'staff': staff}
    return render(request, template, context)

def stafftimesheet(request, template="josstaff/stafftimesheet.html", extra_context=None):
    firstname = request.GET.get('firstname')
    staffmember = get_object_or_404(JOSStaffMember, first_name = firstname)
    context = {'member': staffmember}
    return render(request, template, context)