

from django.shortcuts import render, get_object_or_404
from django.contrib.messages import info, error
from josstaff.models import JOSStaffMember
from django.utils.translation import ugettext_lazy as _

from .forms import JOSStaffHoursEntryForm

# Create your views here.


def staffgallery(request, template="josstaff/staffgallery.html", extra_context= None):
    staff = JOSStaffMember.objects.all()
    context = {'staff': staff}
    return render(request, template, context)


def stafftimesheet(request, template="josstaff/stafftimesheet.html", extra_context=None):
    firstname = request.GET.get('firstname')
    staffmember = get_object_or_404(JOSStaffMember, first_name = firstname)

    form = JOSStaffHoursEntryForm(request.POST or None, request.FILES or None, instance=staffmember)
    context = {'member': staffmember,"form": form}

    if request.method == "POST" and form.is_valid():
        user = form.save()
        info(request, _("Entry accepted"))

    return render(request, template, context)