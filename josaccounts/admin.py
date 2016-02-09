from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from josaccounts.models import JOSProfile

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class JOSProfileInline(admin.StackedInline):
    model = JOSProfile
    can_delete = False
    verbose_name_plural = 'Profiles'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (JOSProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)