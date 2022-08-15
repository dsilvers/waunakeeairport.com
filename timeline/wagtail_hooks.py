from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import PersonTag, EventTag


class PersonAdmin(ModelAdmin):
    model = PersonTag


class EventAdmin(ModelAdmin):
    model = EventTag


modeladmin_register(EventAdmin)
modeladmin_register(PersonAdmin)
