from django.contrib import admin

from .models import *

# Register your models here.

class JOSCourseDayAdmin(admin.ModelAdmin):
    verbose_name = 'Week'
    list_display = ("id", "day_num", "title", "updated")
    readonly_fields = ('created', 'updated',)
admin.site.register(JOSCourseDay, JOSCourseDayAdmin)


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
    list_display = ("id", "author", "wheel", "publish_permission", "auto_save", "updated", "title", "content_start")

    verbose_name = "JOSStory"

    readonly_fields = ("created", "updated",)

    list_editable = ("publish_permission", "auto_save")
admin.site.register(JOSStory, JOSStoryAdmin)


class JOSWheelAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "wheel_story_id", "updated")

    verbose_name = "wheel"

    readonly_fields = ("author", "title", "created", "updated",)

    def wheel_story_id(self, instance):
        return instance.josstory.id
admin.site.register(JOSWheel, JOSWheelAdmin)


class JOSPlotAdmin(admin.ModelAdmin):
    list_display = ("id",  "incite", "rising", "climax", "falling", "resolve", "updated")

    verbose_name = "Plot"

    readonly_fields = ("created", "updated",)
admin.site.register(JOSPlot, JOSPlotAdmin)


class JOSCharacterAdmin(admin.ModelAdmin):
    list_display = ("id",  "updated")

    verbose_name = "Characters"

    readonly_fields = ("created", "updated",)
admin.site.register(JOSCharacter, JOSCharacterAdmin)


class JOSThemeAdmin(admin.ModelAdmin):
    list_display = ("id",  "updated")

    verbose_name = "Characters"

    readonly_fields = ("created", "updated",)
admin.site.register(JOSTheme, JOSThemeAdmin)


class JOSWorldAdmin(admin.ModelAdmin):
    list_display = ("id",  "updated")

    verbose_name = "Characters"

    readonly_fields = ("created", "updated",)
admin.site.register(JOSWorld, JOSWorldAdmin)


class JOSConflictAdmin(admin.ModelAdmin):
    list_display = ("id",  "updated")

    verbose_name = "Characters"

    readonly_fields = ("created", "updated",)
admin.site.register(JOSConflict, JOSConflictAdmin)


class JOSPriorVersionAdmin(admin.ModelAdmin):
    list_display = ("id", "updated", "pv_story", "pv_date", "pv_title", "pv_story_content_start")
    readonly_fields = ("created", "updated",)
admin.site.register(JOSPriorVersion, JOSPriorVersionAdmin)

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
