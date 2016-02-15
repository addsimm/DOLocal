from django.contrib import admin
from josstaff.models import JOSStaffMember

class JOSStaffMemberAdmin(admin.ModelAdmin):
    model = JOSStaffMember

# Register your models here.

admin.site.register(JOSStaffMember, JOSStaffMemberAdmin)
