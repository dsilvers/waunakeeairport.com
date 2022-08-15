from django import forms

from .models import RunwayUseAgreement, WAPASignup


class RunwayUseAgreementForm(forms.ModelForm):
    i_agree = forms.BooleanField(required=True)

    class Meta:
        model = RunwayUseAgreement
        fields = [
            "name",
            "organization",
            "email",
            "phone",
            "address1",
            "address2",
            "city",
            "state",
            "zip_code",
            "tail_number",
            "certificate_level",
            "ifr_rated",
            "i_agree",
        ]


class WAPASignupForm(forms.ModelForm):
    class Meta:
        model = WAPASignup
        exclude = ["signup_datetime"]
