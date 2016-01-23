from django.contrib import admin
from adminsortable.admin import SortableAdmin
from josstaff.models import JOSStaffMember

class JOSStaffMemberAdmin(SortableAdmin):
    model = JOSStaffMember

# Register your models here.

admin.site.register(JOSStaffMember, JOSStaffMemberAdmin)
