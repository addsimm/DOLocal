from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from .models import JOSCourseWeek, JOSHandout

# Create your views here.

@login_required
def course_week_list(request, template="###", extra_context=None):
    weeks = JOSCourseWeek.objects.order_by('week_no')

    context = {'weeks': weeks}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def course_week(request, week_no="0", part_no="9", segment_no="9", handout_id="1", template="joscourses/joshandout.html", extra_context=None):

    week = get_object_or_404(JOSCourseWeek, week_no=int(week_no))
    week_handouts = JOSHandout.objects.filter(courseweek=week, part_no = int(part_no), publish=True)
    week_segments = week_handouts.distinct('segment_no').order_by('segment_no')

    try:
        first_segment_no = week_segments[0].segment_no
    except:
        first_segment_no = 9

    if segment_no != "9":
        current_segment_no = int(segment_no)
    else:
        current_segment_no = first_segment_no

    current_handouts = week_handouts.filter(segment_no=current_segment_no).order_by('element_order')

    if handout_id == '1':
        try:
            cur_handout = current_handouts[0]
        except:
            cur_handout = get_object_or_404(JOSHandout, pk=1)
    else:
        try:
            cur_handout = get_object_or_404(JOSHandout, pk=int(handout_id))
        except:
            cur_handout = get_object_or_404(JOSHandout, pk=1)

    pdf_missing = False
    if not cur_handout.pdf_handout:
        pdf_missing = True

    context = { 'week':       week,
                'part_no': int(part_no),
                'segments':   week_segments,
                'current_segment': current_segment_no,
                'handouts':   current_handouts,
                'handout': cur_handout,
                'pdf_missing': pdf_missing
               }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


# from wand.image import Image
#
# with Image(filename='pikachu.png') as img:
#     print('width =', img.width)
#     print('height =', img.height)

# with Image(filename='pikachu.png') as img:
#     img.format = 'jpeg'
#
# with Image(filename='pikachu.png') as original:
#     with original.convert('jpeg') as converted:
#         # operations to a jpeg image...
#         pass
#
# img.save(filename='pikachu.jpg') //// SAVE LOCALLY


# def content_file_name(instance, filename):
#     return '/'.join(['content', instance.user.username, filename])
#
#
# class Content(models.Model):
#     name = models.CharField(max_length=200)
#     user = models.ForeignKey(User)
#     file = models.FileField(upload_to=content_file_name)