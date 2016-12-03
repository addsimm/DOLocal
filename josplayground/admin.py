from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import JoingoCard

# Register your models here.

class JoingoCardAdmin(admin.ModelAdmin):
    """
    Admin class for JOSProfiles.
    """

    readonly_fields = ('created', 'updated',)

    verbose_name = 'Joingo Card'
    verbose_name_plural = 'Joingo Card'

    # fieldsets = josprofile_fieldsets
    # list_display = josprofile_list_display
    # list_filter = josprofile_list_filter
    # filter_horizontal = ("categories", "related_posts",)


admin.site.register(JoingoCard, JoingoCardAdmin)
