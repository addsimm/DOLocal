from django.template.response import TemplateResponse


### DEVELOPMENT
def playground_view(request, template="playground.html", extra_context=None):
    context = {}
    context.update(extra_context or {})

    return TemplateResponse(request, template, context)


