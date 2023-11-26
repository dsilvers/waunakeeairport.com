import json
import os
from socket import gethostbyaddr
from uuid import UUID

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic.edit import CreateView
from xhtml2pdf import pisa

from .forms import RunwayUseAgreementForm, WAPASignupForm
from .models import RunwayUseAgreement, RunwayUseAgreementDocument


class RunwayUseAgreementView(CreateView):
    form_class = RunwayUseAgreementForm
    template_name = "forms/runway_use_agreement_form.html"
    success_url = "/runway-use-agreement-thanks/"

    def form_valid(self, form):
        submission = form.save(commit=False)

        # Get IP address and reverse DNS
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", "")

        reverse_dns = ""
        if ip:
            try:
                reverse_dns = gethostbyaddr(reverse_dns)[0]
            except Exception:
                reverse_dns = ""

        submission.submit_browser = self.request.headers.get("User-Agent", "")
        submission.submit_ip_address = ip
        submission.submit_reverse_dns = reverse_dns
        submission.save()

        # Generate a PDF
        content = render_to_string(
            "forms/runway_agreement_pdf.html",
            {
                "submission": submission,
                "agreement": RunwayUseAgreementDocument.objects.first(),
            },
        )

        content = (
            content.replace("TODAY", str(submission.submit_datetime.date()))
            .replace("YOUR-NAME", submission.name.upper())
        )

        filename = slugify(f"{submission.name}-{submission.pk}") + ".pdf"
        rua_pdf_file_path = f"{settings.RUA_PDF_ROOT}/{filename}"

        out = open(rua_pdf_file_path, "w+b")
        pisa_status = pisa.CreatePDF(src=content, dest=out)
        out.close()

        if pisa_status.err:
            return HttpResponse(f"Error creating PDF: {pisa_status.err}")

        # Mark this submission as processed
        submission.sns_processed_datetime = timezone.now()
        submission.s3_pdf_filename = filename
        submission.save()

        # Generate email body
        email_body = render_to_string(
            "forms/runway_agreement_email.txt",
            {
                "submission": submission,
            },
        )

        subject_name_tail = submission.name
        if submission.tail_number:
            subject_name_tail = f"{submission.name} [{submission.tail_number}]"

        # Email Us
        email = EmailMessage(
            f"[6P3] Runway Use Agreement Signed - {subject_name_tail}",  # subject
            email_body,
            settings.SERVER_EMAIL,  # From
            to=[settings.RUNWAY_AGREEMENT_SIGNUP_SEND_EMAIL_TO],  # To []
            headers={"Reply-To": submission.email},
        )
        email.attach_file(rua_pdf_file_path)
        email.send(fail_silently=True)

        # Email Them
        email = EmailMessage(
            f"Waunakee Airpark Runway Use Agreement Signed - {subject_name_tail}",  # subject
            email_body,
            settings.SERVER_EMAIL,  # From
            to=[submission.email],  # To []
            headers={"Reply-To": settings.RUNWAY_AGREEMENT_SIGNUP_SEND_EMAIL_TO},
        )
        email.attach_file(rua_pdf_file_path)
        email.send(fail_silently=True)


        return HttpResponseRedirect(self.success_url)

class WAPASignupView(CreateView):
    form_class = WAPASignupForm
    template_name = "forms/wapa_signup.html"
    success_url = "/wapa/thanks/"  # should use reverse(), but wagtail complicates things
