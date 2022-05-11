from django.db import models

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, ItemBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks


class PersonTag(TagBase):
    class Meta:
        verbose_name = "Person Tag"
        verbose_name_plural = "People Tags"


class TaggedPeople(ItemBase):
    tag = models.ForeignKey(
        'timeline.PersonTag', related_name="tagged_people", on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        to='timeline.TimelinePage',
        on_delete=models.CASCADE,
        related_name='tagged_people_items'
    )


class EventTag(TagBase):
    class Meta:
        verbose_name = "Event Tag"
        verbose_name_plural = "Event Tags"


class TaggedEvent(ItemBase):
    tag = models.ForeignKey(
        'timeline.EventTag', related_name="tagged_events", on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        to='timeline.TimelinePage',
        on_delete=models.CASCADE,
        related_name='tagged_event_items'
    )


class PublicationTag(TagBase):
    class Meta:
        verbose_name = "Publication Tag"
        verbose_name_plural = "Publication Tags"


class TaggedPublication(ItemBase):
    tag = models.ForeignKey(
        'timeline.PublicationTag', related_name="tagged_publications", on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        to='timeline.TimelinePage',
        on_delete=models.CASCADE,
        related_name='tagged_publication_items'
    )


class TimelinePage(Page):
    date = models.DateField(blank=True, null=True)
    highlight_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    caption = models.TextField('caption', blank=True)
    body = RichTextField(blank=True)

    content = StreamField(
        [
            ("image", ImageChooserBlock()),
            ("YouTube", blocks.URLBlock()),
            ("VideoMP4", blocks.URLBlock()),
        ]
    )

    people = ClusterTaggableManager('People', through='timeline.TaggedPeople', blank=True)
    events = ClusterTaggableManager('Events', through='timeline.TaggedEvent', blank=True)

    publication = ClusterTaggableManager('Publication Name', through='timeline.TaggedPublication', blank=True)
    byline = models.CharField(max_length=200, blank=True)
    page_or_edition = models.CharField(max_length=200, blank=True)

    photo_credit = models.CharField(max_length=200, blank=True)
    source_url = models.URLField(blank=True)
    copyright_restricted = models.BooleanField(default=False)
    courtesy_of = models.CharField(max_length=200, blank=True)

    document_text = models.TextField(blank=True)

    content_panels = [
        FieldPanel('title'),

        StreamFieldPanel("content"),

        MultiFieldPanel(
            [
                FieldPanel('date'),
                ImageChooserPanel('highlight_image'),
                FieldPanel('caption'),
                FieldPanel('body'),
            ],
            heading="Details",
        ),

        MultiFieldPanel(
            [
                FieldPanel('people'),
                FieldPanel('events'),
            ],
            heading="Tagging",
        ),

        MultiFieldPanel(
            [
                FieldPanel('publication'),
                FieldPanel('byline'),
                FieldPanel('page_or_edition'),
            ],
            heading="Article Details",
        ),

        MultiFieldPanel(
            [
                FieldPanel('photo_credit'),
                FieldPanel('copyright_restricted'),
                FieldPanel('courtesy_of'),
                FieldPanel('source_url'),
            ],
            heading="Copyright Details or Source",
        ),

        MultiFieldPanel(
            [
                FieldPanel('document_text'),
            ],
            heading='SEO/Screen Reader',
        ),

    ]

    @property
    def next_sibling(self):
        objs = TimelinePage.objects.live().order_by('-date').values_list('pk')

        location = None
        next_page_pk = None
        next_page = None

        for pos, value in enumerate(objs):
            if value[0] == self.pk:
                location = pos
                break

        if location is not None:
            try:
                next_page_pk = objs[location + 1][0]
            except IndexError:
                pass

        if next_page_pk:
            next_page = TimelinePage.objects.filter(pk=next_page_pk).first()

        return next_page


class TimelineLandingPage(Page):
    def get_timeline_items(self):
        return TimelinePage.objects.live().order_by('-date')

