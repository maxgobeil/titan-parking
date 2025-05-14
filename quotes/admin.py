from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    BlogPost,
    BusinessVisit,
    Client,
    CustomUser,
    MileageEntry,
    Quote,
    QuoteItem,
    Service,
)


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name", "is_staff")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "job_title")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Business Permissions",
            {
                "fields": (
                    "can_create_quotes",
                    "can_approve_quotes",
                    "can_access_financials",
                )
            },
        ),
        ("Social Auth", {"fields": ("is_social_account", "social_provider")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    extra = 1
    fields = ("service", "quantity", "unit_price", "total_price", "notes")
    readonly_fields = ("total_price",)

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return fields

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return readonly_fields


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_link",
        "title",
        "status",
        "created_at",
        "formatted_total_amount",
    )
    list_filter = ("status", "time_period")
    search_fields = ("client__name", "title")
    inlines = [QuoteItemInline]
    readonly_fields = ("access_token", "verification_code")

    def client_link(self, obj):
        url = reverse("admin:quotes_client_change", args=[obj.client.id])
        return format_html('<a href="{}">{}</a>', url, obj.client.name)

    client_link.short_description = "Client"

    def formatted_total_amount(self, obj):
        amount = "${:,.2f}".format(float(obj.total_amount))
        return format_html("<span>{}</span>", amount)

    formatted_total_amount.short_description = "Total Amount"

    def get_list_display_links(self, request, list_display):
        return ("id", "title")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "default_price", "unit_type", "active")
    list_filter = ("active", "unit_type")
    search_fields = ("name", "description")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "phone")
    search_fields = ("name", "email", "company")


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "published_at", "author_name")
    list_filter = ("status", "author_name")
    search_fields = ("title", "content", "summary")
    list_editable = ("status",)
    list_per_page = 20


@admin.register(MileageEntry)
class MileageEntryAdmin(admin.ModelAdmin):
    list_display = ("date", "trip_purpose", "start_odometer", "end_odometer", "notes")
    list_filter = ("trip_purpose",)
    search_fields = ("notes",)


@admin.register(BusinessVisit)
class BusinessVisitAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "business_name",
        "visit_type",
        "cards_left",
    )
    list_filter = ("visit_type",)
