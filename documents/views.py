import json
import os
from socket import gethostbyaddr
from uuid import UUID

import boto3
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic.edit import CreateView
from xhtml2pdf import pisa

from .forms import RunwayUseAgreementForm, WAPASignupForm
from .models import RunwayUseAgreement, RunwayUseAgreementDocument


class WTF(View):
    def get(self, *args, **kwargs):
        print("HEADERS")
        print(self.request.headers)
        print("META")
        print(self.request.META)

        return HttpResponse("OK")


class RunwayUseAgreementView(CreateView):
    form_class = RunwayUseAgreementForm
    template_name = "forms/runway_use_agreement_form.html"
    success_url = "/runway-use-agreement-thanks/"

    def form_valid(self, form):
        self.object = form.save(commit=False)

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

        self.object.submit_browser = self.request.headers.get("User-Agent", "")
        self.object.submit_ip_address = ip
        self.object.submit_reverse_dns = reverse_dns
        self.object.save()

        # Queue SNS job
        client = boto3.client("sns")
        try:
            response = client.publish(
                TopicArn=settings.SNS_TOPIC_AIRPORT_RUNWAY_AGREEMENT,
                Message=str(self.object.pk),
            )
        except Exception as e:
            print(e)
            pass
        else:
            self.object.sns_message_id = response["MessageId"]
            self.object.sns_queued_datetime = timezone.now()
            self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(csrf_exempt, name="dispatch")
class ProcessRunwayUseAgreementView(View):
    def post(self, *args):
        # We could validate this SNS, but supposedly the methods that AWS uses
        # aren't even all that secure (basically forge the entire message and certs)
        # and you're good to go... huh what?
        try:
            data = json.loads(self.request.body)
        except Exception as e:
            return HttpResponse(f"NOT OK: unable to parse JSON. Error: {e}")

        topic_arn = data.get("TopicArn", None)
        if not topic_arn or topic_arn != settings.SNS_TOPIC_AIRPORT_RUNWAY_AGREEMENT:
            return HttpResponse(f"NOT OK: TopicARN does not match what we are expecting. {topic_arn}")

        sns_message_type = data.get("Type", None)
        if sns_message_type == "SubscriptionConfirmation":
            print("BEGIN VERIFICATION URL")
            print(data.get("SubscribeURL"))
            print("END VERIFICATION URL")
            return HttpResponse("OK for subscription confirmation")

        submission_uuid = data.get("Message", None)
        if not submission_uuid:
            return HttpResponse("NOT OK: UUID is missing from the Message Body")

        try:
            UUID(submission_uuid)
        except ValueError:
            return HttpResponse("NOT OK: invalid UUID")

        try:
            submission = RunwayUseAgreement.objects.get(pk=submission_uuid)
        except RunwayUseAgreement.DoesNotExist:
            return HttpResponse("NOT OK: UUID not found in DB")

        if submission.sns_processed_datetime:
            return HttpResponse("ALREADY PROCESSED")

        # Generate a PDF
        content = render_to_string(
            "forms/runway_agreement_pdf.html",
            {
                "submission": submission,
                "agreement": RunwayUseAgreementDocument.objects.first(),
            },
        )

        tail_number = "(NO TAIL NUMBER SUBMITTED)"
        if submission.tail_number:
            tail_number = submission.tail_number.upper()

        content = (
            content.replace("TODAY", str(submission.submit_datetime.date()))
            .replace("YOUR-NAME", submission.name.upper())
            .replace("YOUR-AIRCRAFT", tail_number)
        )

        filename = slugify(f"{submission.name}-{submission.pk}") + ".pdf"
        temporary_file = f"/tmp/{filename}"

        out = open(temporary_file, "w+b")
        pisa_status = pisa.CreatePDF(src=content, dest=out)
        out.close()

        if pisa_status.err:
            return HttpResponse(f"Error creating PDF: {pisa_status.err}")

        # Upload to S3
        s3 = boto3.client("s3")
        with open(temporary_file, "rb") as f:
            s3.upload_fileobj(f, settings.S3_BUCKET_AIRPORT_RUNWAY_AGREEMENT, filename)

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
        email.attach_file(temporary_file)
        email.send(fail_silently=True)

        # Email Them
        email = EmailMessage(
            f"Waunakee Airpark Runway Use Agreement Signed - {subject_name_tail}",  # subject
            email_body,
            settings.SERVER_EMAIL,  # From
            to=[submission.email],  # To []
            headers={"Reply-To": settings.RUNWAY_AGREEMENT_SIGNUP_SEND_EMAIL_TO},
        )
        email.attach_file(temporary_file)
        email.send(fail_silently=True)

        os.remove(temporary_file)
        return HttpResponse("OK")


class WAPASignupView(CreateView):
    form_class = WAPASignupForm
    template_name = "forms/wapa_signup.html"
    success_url = "/wapa/thanks/"  # should use reverse(), but wagtail complicates things
