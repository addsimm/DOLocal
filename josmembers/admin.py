from __future__ import unicode_literals
from copy import deepcopy

from django.contrib import admin

from josmembers.models import JOSProfile, JOSReservation
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

    verbose_name = 'Member profile'

    readonly_fields = ('created', 'updated',)

    # fieldsets = josprofile_fieldsets
    # list_display = josprofile_list_display
    # list_filter = josprofile_list_filter
    # filter_horizontal = ("categories", "related_posts",)

admin.site.register(JOSProfile, JOSProfileAdmin)


class JOSReservationAdmin(admin.ModelAdmin):
    """
    Admin class for JOSReservations.
    """
    verbose_name = 'Reservation'

    list_display = ("id", "ready", "confirmed", "updated", "first_name", "last_name", "refer")
    list_editable = ("ready", "confirmed")

    readonly_fields = ('updated',)

    # fieldsets = josprofile_fieldsets
    # list_display = josprofile_list_display
    # list_filter = josprofile_list_filter
    # filter_horizontal = ("categories", "related_posts",)


admin.site.register(JOSReservation, JOSReservationAdmin)
