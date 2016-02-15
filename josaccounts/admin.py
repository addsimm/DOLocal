from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.admin import DisplayableAdmin

from josaccounts.models import JOSProfile

# Register your models here.

josprofile_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
josprofile_list_display = ["title", "user", "status", "admin_link"]
josprofile_fieldsets[0][1]["fields"].insert(-2, "profile_photo")
josprofile_list_display.insert(0, "admin_thumb")
josprofile_fieldsets = list(josprofile_fieldsets)


class JOSProfileAdmin(DisplayableAdmin):
    """
    Admin class for JOSProfiles.
    """
    can_delete = True
    verbose_name_plural = 'JOS Profiles'

    fieldsets = josprofile_fieldsets
    list_display = josprofile_list_display
    # list_filter = josprofile_list_filter
    # filter_horizontal = ("categories", "related_posts",)

    def save_form(self, request, form, change):
        """
        Super class ordering is important here - user must get saved first.
        """
        # OwnableAdmin.save_form(self, request, form, change)
        return DisplayableAdmin.save_form(self, request, form, change)


admin.site.register(JOSProfile, JOSProfileAdmin)