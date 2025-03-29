from django.shortcuts import render


def home_view(request):
    return render(request, "pages/index.html")


def terms_view(request):
    return render(request, "pages/terms-of-service.html")


def privacy_view(request):
    return render(request, "pages/privacy-policy.html")


def sitemap_view(request):
    return render(request, "sitemap.xml", content_type="application/xml")


def robots_view(request):
    return render(request, "robots.txt", content_type="text/plain")
