from django.contrib import admin

from .models import CKRichTextHolder, JOSStory

# Register your models here.


class CKRichTextHolderAdmin(admin.ModelAdmin):
    """
    Admin class for CKRichTextEditHolders.
    """
    list_display = ("id", "author", "updated", "parent_class", "parent_id", "field_edited")

    verbose_name = "CKEHolder"

    readonly_fields = ("created", "updated",)

admin.site.register(CKRichTextHolder, CKRichTextHolderAdmin)


class JOSStoryAdmin(admin.ModelAdmin):
    """
    Admin class for JOSStory.
    """
    list_display = ("id", "author", "publish", "updated", "title", "content")

    verbose_name = "JOSStory"

    readonly_fields = ("created", "updated",)

    list_editable = ("publish",)

admin.site.register(JOSStory, JOSStoryAdmin)