from django.db import models
from django.shortcuts import get_object_or_404

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TagBase, ItemBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from modelcluster.models import ClusterableModel


class PersonTag(TagBase):
    name = models.CharField(max_length=200, blank=True, null=True)
    blurb = RichTextField(blank=True)
    image = models.ForeignKey(
        "timeline.WaunakeeImage", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('blurb'),
        ImageChooserPanel('image'),
    ]

    class Meta:
        verbose_name = "Person Tag"
        verbose_name_plural = "People Tags"


class TaggedPeoplePage(ItemBase):
    tag = models.ForeignKey(
        'timeline.PersonTag', related_name="tagged_people_page_tag", on_delete=models.CASCADE,
    )
    content_object = ParentalKey(
        to='timeline.TimelinePage',
        on_delete=models.CASCADE,
        related_name='tagged_people_page',
    )


class EventTag(TagBase):
    name = models.CharField(max_length=200, blank=True, null=True)
    blurb = RichTextField(blank=True)
    image = models.ForeignKey(
        "timeline.WaunakeeImage", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    class Meta:
        verbose_name = "Event Tag"
        verbose_name_plural = "Event Tags"

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('blurb'),
        ImageChooserPanel('image'),
    ]


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
        "timeline.WaunakeeImage", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
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

    people = ClusterTaggableManager('People', through='timeline.TaggedPeoplePage', blank=True)
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


class TimelineLandingPage(RoutablePageMixin, Page):

    def get_pages_qs(self):
        return TimelinePage.objects.live().order_by('-date')

    @route(r'^$')
    def all_timeline(self, request):
        return self.render(
            request,
            context_overrides={
                'title': 'Waunakee Airport Timeline',
                'pages': self.get_pages_qs(),
                'timeline_landing_page': self,
            },
            template="timeline/timeline_landing_page.html",
        )

    @route(r'^person/(?P<person_slug>[\w-]+)')
    def person_timeline(self, request, person_slug):
        person_tag = get_object_or_404(PersonTag, slug=person_slug)

        return self.render(
            request,
            context_overrides={
                'title': person_tag.name,
                'person': person_tag,
                'pages': self.get_pages_qs().filter(people__in=[person_tag]),
                'timeline_landing_page': self,
            },
            template="timeline/timeline_landing_page.html",
        )

    @route(r'^event/(?P<event_slug>[\w-]+)')
    def event_timeline(self, request, event_slug):
        event_tag = get_object_or_404(EventTag, slug=event_slug)

        return self.render(
            request,
            context_overrides={
                'title': event_tag.name,
                'event': event_tag,
                'pages': self.get_pages_qs().filter(events__in=[event_tag]),
                'timeline_landing_page': self,
            },
            template="timeline/timeline_landing_page.html",
        )


class WaunakeeImage(AbstractImage):
    caption = models.CharField(max_length=255, blank=True)
    photo_credit = models.CharField(max_length=200, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'caption',
        'photo_credit',
    )


class WaunakeeImageRendition(AbstractRendition):
    image = models.ForeignKey(WaunakeeImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
