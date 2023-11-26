import uuid

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from localflavor.us.models import USStateField
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet


class CertificateLevelChoices(models.TextChoices):
    ATP = "ATP", "ATP"
    COMMERCIAL = "Commercial", "Commercial"
    PRIVATE = "Private", "Private"
    SPORT = "Sport", "Sport"
    RECREATIONAL = "Recreational", "Recreational"
    STUDENT = "Student", "Student"
    NONE = "No Cert", "No Certificate"


@register_snippet
class RunwayUseAgreementDocument(models.Model):
    content = RichTextField()

    def __str__(self):
        return "Runway Use Agreement"

    class Meta:
        ordering = ["-pk"]


class RunwayUseAgreement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100, blank=True)

    email = models.EmailField()
    phone = models.CharField(max_length=100)

    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, default="Waunakee")
    state = USStateField(default="WI")
    zip_code = models.CharField(max_length=20, default="53597")

    tail_number = models.CharField(max_length=100, blank=True)

    certificate_level = models.CharField(
        max_length=14,
        choices=CertificateLevelChoices.choices,
        default=CertificateLevelChoices.NONE,
    )
    ifr_rated = models.BooleanField(default=False)

    submit_browser = models.CharField(max_length=250, blank=True)
    submit_ip_address = models.GenericIPAddressField(blank=True, null=True)
    submit_reverse_dns = models.CharField(max_length=100, blank=True)
    submit_datetime = models.DateTimeField(auto_now_add=True)

    sns_message_id = models.CharField(max_length=100, blank=True)
    sns_queued_datetime = models.DateTimeField(blank=True, null=True)

    sns_processed_datetime = models.DateTimeField(blank=True, null=True)
    s3_pdf_filename = models.CharField(max_length=100, blank=True)

    def __str__(self):
        if self.organization:
            return f"{self.name} ({self.organization}) [{self.submit_datetime}]"
        return f"{self.name} [{self.submit_datetime}]"


class WAPASignup(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)

    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100, default="Waunakee")
    state = USStateField(default="WI")
    zip_code = models.CharField(max_length=20, default="53597")

    aircraft_year_make_model = models.CharField(max_length=100, blank=True)
    aircraft_n_number = models.CharField(max_length=100, blank=True)
    aircraft_based = models.CharField(max_length=100, blank=True)

    signup_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-signup_datetime"]

    def __str__(self):
        return self.name


@receiver(post_save, sender=RunwayUseAgreement)
def runway_use_agreement_queue_sns(sender, instance, created, **kwargs):
    if created:
        print("created")


@receiver(post_save, sender=WAPASignup)
def wapa_signup_send_email(sender, instance, created, **kwargs):
    if created:
        email = EmailMessage(
            f"[WAPA] New WAPA Signup - {instance.name}",  # subject
            render_to_string("forms/wapa_signup_email.txt", {"signup": instance}),  # Message
            settings.SERVER_EMAIL,  # From
            to=[settings.WAPA_SIGNUP_SEND_EMAIL_TO],  # To []
            headers={"Reply-To": instance.email},
        )
        email.send(fail_silently=True)
