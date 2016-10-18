from django.contrib import admin

from josmessages.models import Message, JOSMessageThread

class MessageAdmin(admin.ModelAdmin):

    list_display = ("id", "message_thread", "sender", "recipient", "subject", "sent_at")
    list_filter  = ("message_thread", "sent_at")

admin.site.register(Message, MessageAdmin)


class JOSMessageThreadAdmin(admin.ModelAdmin):
    """
    Admin class for JOSMessageThread.
    """
    verbose_name = "Thread"
    list_display = ("id", "subject", "message_count", "last_message_id", "updated",)
    list_filter = ("last_recipient",)

    readonly_fields = ("created", "updated",)

admin.site.register(JOSMessageThread, JOSMessageThreadAdmin)
