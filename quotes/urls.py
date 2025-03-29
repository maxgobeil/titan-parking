from django.contrib import admin
from django.urls import path

from . import views  # Import views from the main project

urlpatterns = [
    path("", views.home_view, name="home"),
    path("terms-of-service/", views.terms_view, name="terms-of-service"),
    path("privacy-policy/", views.privacy_view, name="privacy-policy"),
    path("sitemap.xml", views.sitemap_view, name="sitemap"),
    path("robots.txt", views.robots_view, name="robots"),
]
