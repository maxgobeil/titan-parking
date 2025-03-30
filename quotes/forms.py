from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "contact-form-input", "placeholder": "Your name"}
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "contact-form-input", "placeholder": "Your email"}
        ),
    )

    phone = forms.CharField(
        max_length=20,
        required=True,
        # No validators - accept whatever the user enters
        widget=forms.TextInput(
            attrs={
                "class": "contact-form-input",
                "placeholder": "Your phone number",
                "type": "tel",
            }
        ),
    )

    service = forms.ChoiceField(
        choices=[
            ("parking-lot-striping", "Parking Lot Striping"),
            ("indoor-markings", "Indoor Markings"),
            ("pavement-markings", "Pavement Markings"),
            ("layout-design", "Custom Layout Design"),
            ("line-restoration", "Line Restoration"),
            ("line-removal", "Line Removal"),
            ("other", "Other"),
        ],
        required=True,
        widget=forms.Select(attrs={"class": "contact-form-select"}),
    )

    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "contact-form-textarea",
                "placeholder": "Please describe your project needs",
                "rows": "4",
            }
        ),
    )
