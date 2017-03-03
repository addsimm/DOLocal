from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.contrib.messages import info, error
from django.contrib.admin.views.decorators import staff_member_required

from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.email import send_approve_mail

from .models import JOSStaffMember, JOSStaffHoursEntry
from .forms import JOSStaffHoursEntryForm
from request.models import Request

# Create your views here.


def staffgallery(request, template="josstaff/staffgallery.html", extra_context= None):
    staff = JOSStaffMember.objects.all()
    context = {'staff': staff}
    return render(request, template, context)


def legals(request, template="josstaff/legals.html", extra_context=None):
    staff = JOSStaffMember.objects.all()
    context = {}
    return render(request, template, context)


def community_rules(request, template="josstaff/community_rules.html", extra_context=None):
    staff = JOSStaffMember.objects.all()
    context = {}
    return render(request, template, context)


@staff_member_required
def stafftimesheet(request, template="josstaff/stafftimesheet.html", extra_context=None):

    firstname = request.GET.get('firstname')
    staffmember = get_object_or_404(JOSStaffMember, first_name = firstname)
    staffmember_entries = staffmember.josstaffhoursentry_set.all().values('period_date_start', 'period_date_end','hours_claimed', 'time_claim_approved').order_by('period_date_start')


    josstaffhoursentry = JOSStaffHoursEntry(staff_member = staffmember)

    form = JOSStaffHoursEntryForm(instance=josstaffhoursentry)
    context = {"form": form, "member": staffmember, "member_entries": staffmember_entries}

    if request.method == 'POST':
        form = JOSStaffHoursEntryForm(request.POST)
        if form.is_valid():
            form.save()
            # send_approve_mail(request, staffmember)
            info(request, _("Entry accepted"))

    staffmember_total_hours = staffmember_entries.aggregate(Sum('hours_claimed'))['hours_claimed__sum']
    context.update({"total_hours": staffmember_total_hours})

    return render(request, template, context)


@staff_member_required
def josanal(request, template="josstaff/stats.html", extra_context=None):
    requests = Request.objects.all()
    context = {'hello': 'hello',
               'requests': requests}
    return render(request, template, context)








