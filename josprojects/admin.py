from django.contrib import admin

from .models import CKRichTextHolder, JOSStory1, JOSHelpItem

# Register your models here.


class CKRichTextHolderAdmin(admin.ModelAdmin):
    """
    Admin class for CKRichTextEditHolders.
    """
    list_display = ("id", "author", "updated", "parent_id", "field_edited", 'content')

    verbose_name = "CKEHolder"

    list_filter = ("author", 'field_edited')

    readonly_fields = ("created", "updated",)

admin.site.register(CKRichTextHolder, CKRichTextHolderAdmin)


class JOSHelpItemAdmin(admin.ModelAdmin):
    """
    Admin class for JOSHelpItem.
    """
    list_display = ("id", "title", "content")

    verbose_name = "JOSHelpItem"

    list_editable = ("title", "content")


admin.site.register(JOSHelpItem, JOSHelpItemAdmin)


class JOSStory1Admin(admin.ModelAdmin):
    """
    Admin class for JOSStory.
    """
    list_display = ("id", "author", "publish_permission", "updated", "title", "content")

    verbose_name = "JOSStory"

    readonly_fields = ("created", "updated",)

    list_editable = ("publish_permission",)


admin.site.register(JOSStory1, JOSStory1Admin)