# Generated by Django 3.2.12 on 2022-04-15 14:00

import wagtail.core.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0002_wapasignup"),
    ]

    operations = [
        migrations.CreateModel(
            name="RunwayUseAgreementDocument",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", wagtail.core.fields.RichTextField()),
            ],
        ),
    ]