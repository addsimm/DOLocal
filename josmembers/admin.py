from __future__ import unicode_literals
from copy import deepcopy

from django.contrib import admin

from josmembers.models import JOSProfile

    # , CKRichTextEditHolder

# josprofile_fieldsets = deepcopy(admin.ModelAdmin.fieldsets)
# josprofile_list_display = ["title", "user", "status", "admin_link"]
# josprofile_fieldsets[0][1]["fields"].insert(-2, "profile_photo")
# josprofile_list_display.insert(0, "admin_thumb")
# josprofile_fieldsets = list(josprofile_fieldsets)

# Register your models here.

class JOSProfileAdmin(admin.ModelAdmin):
    """
    Admin class for JOSProfiles.
    """

    verbose_name = 'JOS Profile'

    readonly_fields = ('created', 'updated',)

    # fieldsets = josprofile_fieldsets
    # list_display = josprofile_list_display
    # list_filter = josprofile_list_filter
    # filter_horizontal = ("categories", "related_posts",)

admin.site.register(JOSProfile, JOSProfileAdmin)