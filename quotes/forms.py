from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "contact-form-input", "placeholder": _("Your name")}
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "contact-form-input", "placeholder": _("Your email")}
        ),
    )

    phone = forms.CharField(
        max_length=20,
        required=True,
        # No validators - accept whatever the user enters
        widget=forms.TextInput(
            attrs={
                "class": "contact-form-input",
                "placeholder": _("Your phone number"),
                "type": "tel",
            }
        ),
    )

    service = forms.ChoiceField(
        choices=[
            ("parking-lot-striping", _("Parking Lot Striping")),
            ("indoor-markings", _("Indoor Markings")),
            ("pavement-markings", _("Pavement Markings")),
            ("layout-design", _("Custom Layout Design")),
            ("line-restoration", _("Line Restoration")),
            ("line-removal", _("Line Removal")),
            ("other", _("Other")),
        ],
        required=True,
        widget=forms.Select(attrs={"class": "contact-form-select"}),
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "contact-form-textarea",
                "placeholder": _("Please describe your project needs"),
                "rows": "4",
            }
        ),
    )
