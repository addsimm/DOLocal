from django.contrib import admin

from .models import CKRichTextHolder

# Register your models here.

class CKRichTextHolderAdmin(admin.ModelAdmin):
    """
    Admin class for CKRichTextEditHolders.
    """
    list_display = ("id", "author", "created", "title", "field_to_edit")

    verbose_name = 'CKEditor Text Holder'

    readonly_fields = ('created', 'updated',)


admin.site.register(CKRichTextHolder, CKRichTextHolderAdmin)