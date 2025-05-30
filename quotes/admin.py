from django import forms
from django.contrib import admin, messages
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


class QuoteItemInlineForm(forms.ModelForm):
    class Meta:
        model = QuoteItem
        fields = "__all__"
        widgets = {
            "service": forms.Select(attrs={"style": "width: 200px;"}),
        }


class QuoteItemInline(admin.TabularInline):
    model = QuoteItem
    form = QuoteItemInlineForm
    extra = 0
    fields = ("service", "quantity", "unit_price", "total_price", "notes")
    readonly_fields = ("total_price",)

    def has_add_permission(self, request, obj=None):
        if obj and obj.status in QuoteAdmin.LOCKED_STATUSES:
            return False
        return super().has_add_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj and obj.status in QuoteAdmin.LOCKED_STATUSES:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status in QuoteAdmin.LOCKED_STATUSES:
            return False
        return super().has_delete_permission(request, obj)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields["service"].widget.can_add_related = False
        formset.form.base_fields["service"].widget.can_change_related = False
        formset.form.base_fields["service"].widget.can_delete_related = False
        return formset

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
        "invoice_number",
        "client_company",
        "title",
        "status",
        "created_at",
        "formatted_total_amount",
    )
    list_filter = ("status", "time_period")
    search_fields = ("client__name", "title")
    inlines = [QuoteItemInline]
    readonly_fields = ("access_token", "verification_code")
    actions = ["create_modification", "create_invoice"]

    LOCKED_STATUSES = ["modified", "accepted", "declined", "sent", "expired", "invoice"]

    def has_change_permission(self, request, obj=None):
        if obj and obj.status in self.LOCKED_STATUSES:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.status in self.LOCKED_STATUSES:
            return False
        return super().has_delete_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))

        if obj and obj.status in self.LOCKED_STATUSES:
            # Make all fields readonly except the ones that are already readonly
            all_fields = [field.name for field in obj._meta.fields]
            readonly_fields.extend(
                [field for field in all_fields if field not in readonly_fields]
            )

        return readonly_fields

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}

        if object_id:
            try:
                obj = self.get_object(request, object_id)
                if obj and obj.status in self.LOCKED_STATUSES:
                    messages.warning(
                        request,
                        f"This quote is in '{obj.get_status_display()}' status and cannot be edited. "
                        f"You can only view the details.",
                    )
            except:
                pass

        return super().changeform_view(request, object_id, form_url, extra_context)

    def client_company(self, obj):
        # Show company if available, otherwise show client name
        return obj.client.company if obj.client.company else obj.client.name

    client_company.short_description = "Client/Company"

    def formatted_total_amount(self, obj):
        amount = "${:,.2f}".format(float(obj.total_amount))
        return format_html("<span>{}</span>", amount)

    formatted_total_amount.short_description = "Total Amount"

    def create_modification(self, request, queryset):
        if queryset.count() != 1:
            messages.error(request, "Please select exactly one quote to modify.")
            return

        quote = queryset.first()
        try:
            if not quote.can_be_modified:
                messages.error(
                    request, f"Quote {quote.invoice_number} cannot be modified."
                )
            else:
                new_quote = quote.create_modification()
                messages.success(
                    request,
                    f"Created modification {new_quote.invoice_number} from {quote.invoice_number}",
                )
        except Exception as e:
            messages.error(request, f"Error creating modification: {str(e)}")

    create_modification.short_description = "Create modification from this quote"

    def create_invoice(self, request, queryset):
        if queryset.count() != 1:
            messages.error(request, "Please select exactly one quote to invoice.")
            return

        quote = queryset.first()
        try:
            if not quote.can_be_invoiced:
                messages.error(
                    request, f"Quote {quote.invoice_number} cannot be invoiced."
                )
            else:
                invoice = quote.create_invoice()
                messages.success(
                    request,
                    f"Created invoice {invoice.invoice_number} from quote {quote.invoice_number}",
                )
        except Exception as e:
            messages.error(request, f"Error creating invoice: {str(e)}")

    create_invoice.short_description = "Create invoice from this quote"

    def get_list_display_links(self, request, list_display):
        return ("id", "title")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # If it's a new quote (obj is None) and invoice_number field exists
        if obj is None and "invoice_number" in form.base_fields:
            # Create a temporary quote instance to generate the number
            temp_quote = Quote()
            form.base_fields["invoice_number"].initial = (
                temp_quote.generate_invoice_number()
            )

        return form


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
