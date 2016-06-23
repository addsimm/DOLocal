from django.contrib import admin
from .models import JOSStaffMember, JOSStaffHoursEntry, JOSReferral


class JOSStaffHoursEntryInLine(admin.TabularInline):
    model = JOSStaffHoursEntry
    extra = 0


class JOSStaffHoursEntryAdmin(admin.ModelAdmin):
    model = JOSStaffHoursEntry
    list_display = ('staff_member', 'created', 'period_date_start', 'period_date_end',
                    'hours_claimed', 'time_claim_approved',)
    list_editable = ('time_claim_approved',)
    list_filter = ('staff_member', 'time_claim_approved')

    verbose_name = 'Hours entry'
    verbose_name_plural = 'Hours entries'
    # list_display_links = ('staff_member',)

admin.site.register(JOSStaffHoursEntry, JOSStaffHoursEntryAdmin)


class JOSStaffMemberAdmin(admin.ModelAdmin):
    model = JOSStaffMember
    list_display = ("first_name", "cumalative_hours", "_Hours_Entries_Total", "_Hours_Entries_Open")
    verbose_name = 'Staff member'

    inlines = [JOSStaffHoursEntryInLine]

    def _Hours_Entries_Total(self, obj):
        return obj.josstaffhoursentry_set.all().count()

    def _Hours_Entries_Open(self, obj):
        return obj.josstaffhoursentry_set.filter(time_claim_approved = False).count()

admin.site.register(JOSStaffMember, JOSStaffMemberAdmin)


class JOSReferralAdmin(admin.ModelAdmin):
    model = JOSReferral

    list_display = ("id", "staff_member", "first_name", "last_name", "referral_city")

    verbose_name = 'Referral'

    readonly_fields = ('created', 'updated',)

admin.site.register(JOSReferral, JOSReferralAdmin)






