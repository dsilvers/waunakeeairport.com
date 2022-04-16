from django import template

from documents.models import RunwayUseAgreementDocument

register = template.Library()


@register.inclusion_tag("tags/runwayagreement_tags.html", takes_context=True)
def runwayagreement(context):
    return {
        "runwayagreement": RunwayUseAgreementDocument.objects.first(),
        "request": context["request"],
    }
