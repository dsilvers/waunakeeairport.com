from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel # , StreamFieldPanel
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet


class WaunakeeAirportPageBaseMixin(models.Model):
    hero_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    hero_video_url = models.CharField(max_length=255, blank=True)

    og_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Open Graph preview image (should be a square)",
    )

    promote_panels = Page.promote_panels + [
        FieldPanel("hero_image"),
        FieldPanel("hero_video_url"),
        FieldPanel("og_image"),
    ]

    class Meta:
        abstract = True


# Menu System
# https://learnwagtail.com/tutorials/how-to-create-a-custom-wagtail-menu-system/
class MenuItem(Orderable):
    menu_label = models.CharField(blank=True, null=True, max_length=50)

    link_url = models.CharField(max_length=500, blank=True)

    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
    )

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("menu_label"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return "#"

    @property
    def title(self):
        if self.link_page and not self.menu_label:
            return self.link_page.title
        elif self.menu_label:
            return self.menu_label
        return "Missing Title"


@register_snippet
class Menu(ClusterableModel):
    """The main menu clusterable model."""

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)
    # slug = models.SlugField()

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
            ],
            heading="Menu",
        ),
        InlinePanel("menu_items", label="Menu Item"),
    ]

    def __str__(self):
        return self.title


class HomePageCardBlock(blocks.StructBlock):
    name = blocks.CharBlock(max_length=120)
    blurb = blocks.RichTextBlock()
    button = blocks.CharBlock(max_length=120)
    image = ImageChooserBlock()
    page = blocks.PageChooserBlock()

    class Meta:
        template = "streams/homepage_card.html"
        icon = "image"


class HomePage(WaunakeeAirportPageBaseMixin, Page):
    tagline = models.CharField(max_length=255)
    cards = StreamField(
        [
            ("card", HomePageCardBlock()),
        ], use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("tagline"),
        FieldPanel("cards"),
    ]


class ContentPage(WaunakeeAirportPageBaseMixin, Page):
    name = models.CharField(max_length=255)
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("body", classname="full"),
    ]


class PilotAirportInfoPage(WaunakeeAirportPageBaseMixin, Page):
    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class PancakePage(WaunakeeAirportPageBaseMixin, Page):
    pass
