import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from weasyprint import HTML

from .forms import ContactForm
from .models import BlogPost, Quote


def home_view(request):
    return render(request, "pages/index.html", {"form": ContactForm()})


def about_view(request):
    return render(request, "pages/about.html")


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


def blog_list(request):
    posts = BlogPost.objects.filter(status="published").order_by("-published_at")

    featured_post = None
    other_posts = []

    if posts.exists():
        featured_post = posts.first()
        other_posts = posts[1:]

    popular_posts = BlogPost.objects.filter(status="published").order_by(
        "-published_at"
    )[:5]

    return render(
        request,
        "pages/blog.html",
        {
            "featured_post": featured_post,
            "other_posts": other_posts,
            "popular_posts": popular_posts,
        },
    )


def blog_search(request):
    query = request.GET.get("q", "")

    if query:
        results = BlogPost.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(summary__icontains=query),
            status="published",
        ).order_by("-published_at")
    else:
        results = []

    popular_posts = BlogPost.objects.filter(status="published").order_by(
        "-published_at"
    )[:5]

    return render(
        request,
        "pages/blog-search.html",
        {
            "query": query,
            "results": results,
            "popular_posts": popular_posts,
        },
    )


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status="published")

    next_post = (
        BlogPost.objects.filter(published_at__gt=post.published_at, status="published")
        .order_by("published_at")
        .first()
    )

    prev_post = (
        BlogPost.objects.filter(published_at__lt=post.published_at, status="published")
        .order_by("-published_at")
        .first()
    )

    # Get related posts - for now, just get recent posts
    related_posts = (
        BlogPost.objects.filter(status="published")
        .exclude(id=post.id)
        .order_by("-published_at")[:2]
    )

    popular_posts = (
        BlogPost.objects.filter(status="published")
        .exclude(id=post.id)
        .order_by("-published_at")[:5]
    )

    return render(
        request,
        "pages/blog-detail.html",
        {
            "post": post,
            "next_post": next_post,
            "prev_post": prev_post,
            "related_posts": related_posts,
            "popular_posts": popular_posts,
        },
    )
