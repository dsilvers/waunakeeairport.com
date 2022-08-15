# Generated by Django 3.2.13 on 2022-05-11 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import taggit.managers
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.core.models.collections
import wagtail.images.blocks
import wagtail.images.models
import wagtail.search.index


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailcore', '0066_collection_management_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('blurb', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Event Tag',
                'verbose_name_plural': 'Event Tags',
            },
        ),
        migrations.CreateModel(
            name='PersonTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('blurb', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'verbose_name': 'Person Tag',
                'verbose_name_plural': 'People Tags',
            },
        ),
        migrations.CreateModel(
            name='PublicationTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Publication Tag',
                'verbose_name_plural': 'Publication Tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedPeopleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedPeoplePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaggedPublication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TimelineLandingPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='WaunakeeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_upload_to, verbose_name='file', width_field='width')),
                ('width', models.IntegerField(editable=False, verbose_name='width')),
                ('height', models.IntegerField(editable=False, verbose_name='height')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('focal_point_x', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_y', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_width', models.PositiveIntegerField(blank=True, null=True)),
                ('focal_point_height', models.PositiveIntegerField(blank=True, null=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('file_hash', models.CharField(blank=True, editable=False, max_length=40)),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('photo_credit', models.CharField(blank=True, max_length=200)),
                ('collection', models.ForeignKey(default=wagtail.core.models.collections.get_root_collection_id, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.collection', verbose_name='collection')),
                ('people', modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='timeline.TaggedPeopleImage', to='timeline.PersonTag', verbose_name='People')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text=None, through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('uploaded_by_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.images.models.ImageFileMixin, wagtail.search.index.Indexed, models.Model),
        ),
        migrations.CreateModel(
            name='TimelinePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('date', models.DateField(blank=True, null=True)),
                ('caption', models.TextField(blank=True, verbose_name='caption')),
                ('body', wagtail.core.fields.RichTextField(blank=True)),
                ('content', wagtail.core.fields.StreamField([('image', wagtail.images.blocks.ImageChooserBlock()), ('YouTube', wagtail.core.blocks.URLBlock()), ('VideoMP4', wagtail.core.blocks.URLBlock())])),
                ('byline', models.CharField(blank=True, max_length=200)),
                ('page_or_edition', models.CharField(blank=True, max_length=200)),
                ('photo_credit', models.CharField(blank=True, max_length=200)),
                ('source_url', models.URLField(blank=True)),
                ('copyright_restricted', models.BooleanField(default=False)),
                ('courtesy_of', models.CharField(blank=True, max_length=200)),
                ('document_text', models.TextField(blank=True)),
                ('events', modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='timeline.TaggedEvent', to='timeline.EventTag', verbose_name='Events')),
                ('highlight_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='timeline.waunakeeimage')),
                ('people', modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='timeline.TaggedPeoplePage', to='timeline.PersonTag', verbose_name='People')),
                ('publication', modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='timeline.TaggedPublication', to='timeline.PublicationTag', verbose_name='Publication Name')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='taggedpublication',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_publication_items', to='timeline.timelinepage'),
        ),
        migrations.AddField(
            model_name='taggedpublication',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_publications', to='timeline.publicationtag'),
        ),
        migrations.AddField(
            model_name='taggedpeoplepage',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_people_page', to='timeline.timelinepage'),
        ),
        migrations.AddField(
            model_name='taggedpeoplepage',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_people_page_tag', to='timeline.persontag'),
        ),
        migrations.AddField(
            model_name='taggedpeopleimage',
            name='content_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_people_image', to='timeline.waunakeeimage'),
        ),
        migrations.AddField(
            model_name='taggedpeopleimage',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_people_image_tag', to='timeline.persontag'),
        ),
        migrations.AddField(
            model_name='taggedevent',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_event_items', to='timeline.timelinepage'),
        ),
        migrations.AddField(
            model_name='taggedevent',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_events', to='timeline.eventtag'),
        ),
        migrations.AddField(
            model_name='persontag',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='timeline.waunakeeimage'),
        ),
        migrations.AddField(
            model_name='eventtag',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='timeline.waunakeeimage'),
        ),
        migrations.CreateModel(
            name='WaunakeeImageRendition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_spec', models.CharField(db_index=True, max_length=255)),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.images.models.get_rendition_upload_to, width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(blank=True, default='', editable=False, max_length=16)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='renditions', to='timeline.waunakeeimage')),
            ],
            options={
                'unique_together': {('image', 'filter_spec', 'focal_point_key')},
            },
            bases=(wagtail.images.models.ImageFileMixin, models.Model),
        ),
    ]
