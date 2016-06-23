from __future__ import unicode_literals
from copy import deepcopy

from django.contrib import admin

from josmembers.models import JOSProfile

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