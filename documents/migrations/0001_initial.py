# Generated by Django 3.2.12 on 2022-04-08 02:49

import uuid

import localflavor.us.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RunwayUseAgreement",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("organization", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=100)),
                ("address1", models.CharField(max_length=250)),
                ("address2", models.CharField(blank=True, max_length=250)),
                ("city", models.CharField(default="Waunakee", max_length=100)),
                ("state", localflavor.us.models.USStateField(default="WI", max_length=2)),
                ("zip_code", models.CharField(default="53597", max_length=20)),
                ("tail_number", models.CharField(blank=True, max_length=100)),
                (
                    "certificate_level",
                    models.CharField(
                        choices=[
                            ("ATP", "ATP"),
                            ("Commercial", "Commercial"),
                            ("Private", "Private"),
                            ("Sport", "Sport"),
                            ("Recreational", "Recreational"),
                            ("Student", "Student"),
                            ("No Cert", "No Certificate"),
                        ],
                        default="No Cert",
                        max_length=14,
                    ),
                ),
                ("ifr_rated", models.BooleanField(default=False)),
                ("certificate_number", models.CharField(blank=True, max_length=30)),
                ("submit_browser", models.CharField(blank=True, max_length=250)),
                ("submit_ip_address", models.GenericIPAddressField()),
                ("submit_datetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
