# Generated by Django 3.2.13 on 2022-05-11 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0003_alter_taggedpeopleimage_content_object'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waunakeeimage',
            name='people',
        ),
        migrations.DeleteModel(
            name='TaggedPeopleImage',
        ),
    ]
