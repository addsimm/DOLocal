from django.contrib import admin

from .models import CKRichTextHolder, JOSStory

# Register your models here.


class CKRichTextHolderAdmin(admin.ModelAdmin):
    """
    Admin class for CKRichTextEditHolders.
    """
    list_display = ("id", "author", "created", "class_to_edit", "id_to_edit", "field_to_edit")

    verbose_name = 'CKEditor Text Holder'

    readonly_fields = ('created', 'updated',)


admin.site.register(CKRichTextHolder, CKRichTextHolderAdmin)


class JOSStoryAdmin(admin.ModelAdmin):
    """
    Admin class for JOSStory.
    """
    list_display = ("id", "author", "created", "title")

    verbose_name = 'JOSStory'

    readonly_fields = ('created', 'updated',)


admin.site.register(JOSStory, JOSStoryAdmin)