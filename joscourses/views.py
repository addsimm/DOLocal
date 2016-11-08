from django.core.files import File
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from wand.image import Image
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

    if not cur_handout.image_handout and pdf_missing == False:
        with Image(filename=cur_handout.pdf_handout.path) as  original:
            with original.convert('jpg') as converted:

                format = converted.format
                converted.save(filename='static/img/temporary.jpg')

                f_name="bsho-image-" + str(cur_handout.id)
                cur_handout.image_handout.save(f_name, File(open('static/img/temporary.jpg', 'r')))
                cur_handout.save()

    context = {
        'week':            week,
        'part_no':         int(part_no),
        'segments':        week_segments,
        'current_segment': current_segment_no,
        'handouts':        current_handouts,
        'handout':         cur_handout,
        'pdf_missing':     pdf_missing
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


@login_required
def course_week_test(request, week_no="0", part_no="9", segment_no="9", handout_id="1",
                template="joscourses/testjoshandout.html", extra_context=None):
    week = get_object_or_404(JOSCourseWeek, week_no=int(week_no))
    week_handouts = JOSHandout.objects.filter(courseweek=week, part_no=int(part_no), publish=True)
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

    frmt = 'missing'
    # if not cur_handout.image_handout:
    with Image(filename=cur_handout.pdf_handout.path) as  original:
        with original.convert('png24') as converted:

            converted.save(filename='static/img/temporary.png')
            frmt = converted.format
            f_name = "bsho-image-" + str(cur_handout.id) + '.png'
            cur_handout.image_handout.save(f_name, File(open('static/img/temporary.png', 'r')))
            cur_handout.save()

    context = {
        'week':            week,
        'part_no':         int(part_no),
        'segments':        week_segments,
        'current_segment': current_segment_no,
        'handouts':        current_handouts,
        'handout':         cur_handout,
        'pdf_missing':     pdf_missing,
        'format': frmt
    }

    context.update(extra_context or {})

    return TemplateResponse(request, template, context)