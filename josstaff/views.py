

from django.shortcuts import render, get_object_or_404
from django.contrib.messages import info, error
from josstaff.models import JOSStaffMember
from django.utils.translation import ugettext_lazy as _
from django.core import serializers

from mezzanine.utils.email import send_approve_mail

from .models import JOSStaffMember, JOSStaffHoursEntry
from .forms import JOSStaffHoursEntryForm

# Create your views here.


def staffgallery(request, template="josstaff/staffgallery.html", extra_context= None):
    staff = JOSStaffMember.objects.all()
    context = {'staff': staff}
    return render(request, template, context)


def stafftimesheet(request, template="josstaff/stafftimesheet.html", extra_context=None):

    firstname = request.GET.get('firstname')
    staffmember = get_object_or_404(JOSStaffMember, first_name = firstname)
    #smes = JOSStaffHoursEntry.objects.filter(staff_member_id=staffmember.id)
    smes = staffmember.josstaffhoursentry_set.all()




    staffmember_entries = serializers.serialize("python", smes)


    form = JOSStaffHoursEntryForm(instance=request.user)
    context = {"form": form, 'member': staffmember,
               "smes": smes, "staffmember_entries": staffmember_entries}

    if request.method == 'POST':
        form = JOSStaffHoursEntryForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            send_approve_mail(request, staffmember)
            info(request, _("Entry accepted"))

    return render(request, template, context)






