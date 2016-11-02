from __future__ import unicode_literals

from django.contrib import admin

from josmembers.models import JOSProfile, JOSReservation, JOSTeam
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# from notification.models import NoticeQueueBatch, NoticeSetting, NoticeType
#
# admin.site.unregister(NoticeQueueBatch)
# admin.site.unregister(NoticeSetting)
# admin.site.unregister(NoticeType)

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "id", "email", "is_staff", "last_login")
    list_filter = ("is_staff",)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class JOSProfileAdmin(admin.ModelAdmin):
    """
    Admin class for JOSProfiles.
    """
    model = JOSProfile
    verbose_name = 'User profile'

    list_display = ("id", "user", "last_login", "get_teams", "has_teams")
    readonly_fields = ('created', 'updated',)
    filter_horizontal = ('teams',)

    # def get_teams(self, obj):
    #      return  ", ".join( team.name for team in obj.teams.all())
    #
    # def has_teams(self, obj):
    #     if len(self.get_teams(obj)) > 0:
    #         return True
    #
    #     return False

    def last_login(self, obj):
        return obj.user.last_login

    # fieldsets = josprofile_fieldsets


admin.site.register(JOSProfile, JOSProfileAdmin)


class JOSTeamAdmin(admin.ModelAdmin):
    """
    Admin class for JOSReservations.
    """
    verbose_name = 'Team'

    list_display = ("id", "name", "member_id_list")

    readonly_fields = ("member_id_list", 'created', 'updated',)


admin.site.register(JOSTeam, JOSTeamAdmin)


class JOSReservationAdmin(admin.ModelAdmin):
    """
    Admin class for JOSReservations.
    """
    verbose_name = 'Reservation'

    list_display = ("id", "status", "updated", "first_name", "last_name", "refer")
    list_editable = ("status",)

    readonly_fields = ('updated',)

admin.site.register(JOSReservation, JOSReservationAdmin)
