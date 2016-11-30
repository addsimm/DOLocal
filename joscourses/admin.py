from django.contrib import admin

# Register your models here.

from .models import JOSStory, JOSCourseWeek, JOSHandout, JOSWheel, JOSPlotTemplate, JOSCharacter


# Register your models here.

"""
class JOSStoryActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created", "course", "week")
    verbose_name = 'JOS Story Activity'
    readonly_fields = ('created', 'updated',)


admin.site.register(JOSStoryActivity, JOSStoryActivityAdmin)

class JOSCourseStudentAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "created", "course")
    verbose_name = 'JOS Course Student'
    readonly_fields = ('created', 'updated',)

admin.site.register(JOSCourseStudent, JOSCourseStudentAdmin)

class JOSCourseAdmin(admin.ModelAdmin):
    list_display = ("id", "course_title", "instructor", "updated")
    verbose_name = 'Course'
    readonly_fields = ('created', 'updated',)

admin.site.register(JOSCourse, JOSCourseAdmin)
"""

class JOSCourseWeekAdmin(admin.ModelAdmin):
    verbose_name = 'Week'
    list_display = ("id", "week_no", "week_title", "course", "updated")
    readonly_fields = ('created', 'updated',)

admin.site.register(JOSCourseWeek, JOSCourseWeekAdmin)


class JOSHandoutAdmin(admin.ModelAdmin):
    verbose_name = 'Handout'
    list_display = ("id", "publish", "pdf_handout", "courseweek", "part_no", "segment_no",
                    "element_no", "element_order", "updated",)
    list_editable = ("publish", "pdf_handout", "courseweek", "part_no", "segment_no",
                     "element_no", "element_order")
    readonly_fields = ('created', 'updated',)

    list_filter = ("courseweek", "segment_no", "element_no",)

admin.site.register(JOSHandout, JOSHandoutAdmin)


class JOSStoryAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "publish_permission", "updated", "title", "content")

    verbose_name = "JOSStory"

    readonly_fields = ("created", "updated",)

    list_editable = ("publish_permission",)

admin.site.register(JOSStory, JOSStoryAdmin)


class JOSWheelAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "publish_permission", "updated", "title")

    verbose_name = "wheel"

    readonly_fields = ("created", "updated",)

    list_editable = ("publish_permission",)

admin.site.register(JOSWheel, JOSWheelAdmin)


class JOSPlotTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", 'wheel', "incite", "rising", "climax", "falling", "resolve", "updated")

    verbose_name = "Plot"

    readonly_fields = ("created", "updated",)

admin.site.register(JOSPlotTemplate, JOSPlotTemplateAdmin)


class JOSCharacterAdmin(admin.ModelAdmin):
    list_display = ("id", 'wheel', "nick_name", "first_name", "last_name", "updated")

    verbose_name = "Characters"

    readonly_fields = ("created", "updated",)


admin.site.register(JOSCharacter, JOSCharacterAdmin)