from django.contrib import admin
from josstaff.models import JOSStaffMember

from mezzanine.core.admin import TabularDynamicInlineAdmin

class JOSStaffMemberAdmin(admin.ModelAdmin):
    model = JOSStaffMember

# Register your models here.

admin.site.register(JOSStaffMember, JOSStaffMemberAdmin)