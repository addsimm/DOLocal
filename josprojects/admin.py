from django.contrib import admin

from .models import CKRichTextHolder, JOSStory

# Register your models here.


class CKRichTextHolderAdmin(admin.ModelAdmin):
    """
    Admin class for CKRichTextEditHolders.
    """
    list_display = ("id", "author", "created", "parent_class", "parent_id", "field_edited")

    verbose_name = "JOS CKE Holder"

    readonly_fields = ("created", "updated",)


admin.site.register(CKRichTextHolder, CKRichTextHolderAdmin)


class JOSStoryAdmin(admin.ModelAdmin):
    """
    Admin class for JOSStory.
    """
    list_display = ("id", "author", "created", "title", "content")

    verbose_name = "JOSStory"

    readonly_fields = ("created", "updated",)


admin.site.register(JOSStory, JOSStoryAdmin)