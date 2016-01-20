from django.contrib import admin
from orderable.admin import OrderableAdmin, OrderableTabularInline
from josstaff.models import JOSStaffMember

class JOSStaffMemberAdmin(OrderableAdmin):
    model = JOSStaffMember
    list_display = ('__unicode__', 'sort_order_display')

# Register your models here.

admin.site.register(JOSStaffMember, JOSStaffMemberAdmin)