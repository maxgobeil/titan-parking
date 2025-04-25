import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import ContactForm
from .models import Quote


def home_view(request):
    return render(request, "pages/index.html", {"form": ContactForm()})


def page_not_found_view(request, exception=None):
    return render(request, "pages/404.html", status=404)


@login_required
def terms_view(request):
    return render(request, "pages/terms-of-service.html")


def privacy_view(request):
    return render(request, "pages/privacy-policy.html")


def sitemap_view(request):
    return render(request, "sitemap.xml", content_type="application/xml")


def robots_view(request):
    return render(request, "robots.txt", content_type="text/plain")


def submit_contact(request):
    """View to handle contact form submission"""
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            # Get cleaned data
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            service = form.cleaned_data["service"]
            message_content = form.cleaned_data["message"]

            # Get service display name
            service_display = dict(form.fields["service"].choices)[service]

            # Create email content
            subject = f"New Quote Request: {service_display}"
            email_body = f"""
            New quote request from the website:
            
            Name: {name}
            Email: {email}
            Phone: {phone}
            Service: {service_display}
            
            Message:
            {message_content}
            """

            try:
                send_mail(
                    subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                # Return success message for HTMX
                return render(request, "partials/home/contact-success.html")
            except Exception as e:
                # Handle email sending error
                return render(request, "partials/home/error-message.html")
        else:
            # Form is not valid, return errors
            return render(request, "partials/home/form-errors.html", {"form": form})

    # If not a POST request, return an empty response
    return HttpResponse("")


@login_required
def invoice_view_pdf(request):
    quote = (
        Quote.objects.select_related("client")
        .prefetch_related("items__service")
        .get(id=1)
    )

    image_path = os.path.join(
        settings.BASE_DIR,
        "quotes",
        "templates",
        "quotes",
        "pdf",
        "assets",
        "invoice-header.png",
    )
    # Read CSS
    css_path = os.path.join(
        settings.BASE_DIR,
        "quotes",
        "templates",
        "quotes",
        "pdf",
        "assets",
        "quote_template.css",
    )

    import base64

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    with open(css_path) as f:
        css_data = f.read()

    context = {
        "image_data": image_data,
        "css_data": css_data,
        "quote": quote,
    }

    # Render HTML content
    html_string = render_to_string("quotes/pdf/quote_template.html", context)

    # Create PDF response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="quote.pdf"'

    # Generate PDF
    HTML(string=html_string).write_pdf(response)

    return response


@login_required
def invoice_view_html(request):
    quote = (
        Quote.objects.select_related("client")
        .prefetch_related("items__service")
        .get(id=1)
    )

    image_path = os.path.join(
        settings.BASE_DIR,
        "quotes",
        "templates",
        "quotes",
        "pdf",
        "assets",
        "invoice-header.png",
    )
    # Read CSS
    css_path = os.path.join(
        settings.BASE_DIR,
        "quotes",
        "templates",
        "quotes",
        "pdf",
        "assets",
        "quote_template.css",
    )

    import base64

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    with open(css_path) as f:
        css_data = f.read()

    context = {
        "image_data": image_data,
        "css_data": css_data,
        "quote": quote,
    }

    return render(request, "quotes/pdf/quote_template.html", context)
