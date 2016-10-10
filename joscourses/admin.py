from django.contrib import admin

# Register your models here.

from .models import JOSCourse, JOSCourseStudent, JOSCourseWeek, JOSHandout, JOSStoryActivity


# Register your models here.

class JOSCourseAdmin(admin.ModelAdmin):
    list_display = ("id", "course_title", "instructor", "updated")
    verbose_name = 'Course'
    readonly_fields = ('created', 'updated',)

admin.site.register(JOSCourse, JOSCourseAdmin)


# class JOSCourseStudentAdmin(admin.ModelAdmin):
#     list_display = ("id", "username", "created", "course")
#     verbose_name = 'JOS Course Student'
#     readonly_fields = ('created', 'updated',)
#
# admin.site.register(JOSCourseStudent, JOSCourseStudentAdmin)


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

# class JOSStoryActivityAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "created", "course", "week")
#     verbose_name = 'JOS Story Activity'
#     readonly_fields = ('created', 'updated',)
#
#
# admin.site.register(JOSStoryActivity, JOSStoryActivityAdmin)