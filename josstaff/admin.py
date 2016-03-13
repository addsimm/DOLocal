from django.contrib import admin
from .models import JOSStaffMember, JOSStaffHoursEntry


class JOSStaffHoursEntryAdmin(admin.ModelAdmin):
    model = JOSStaffHoursEntry



class JOSStaffMemberAdmin(admin.StackedInline):
    model = JOSStaffMember
    inlines = [JOSStaffHoursEntry]

# Register your models here.

admin.site.register(JOSStaffHoursEntry, JOSStaffHoursEntryAdmin)
admin.site.register(JOSStaffMember, JOSStaffMemberAdmin)
