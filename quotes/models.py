from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # Business-specific fields
    job_title = models.CharField(_("job title"), max_length=100, blank=True)
    can_create_quotes = models.BooleanField(default=False)
    can_approve_quotes = models.BooleanField(default=False)
    can_access_financials = models.BooleanField(default=False)

    # For social auth
    is_social_account = models.BooleanField(default=False)
    social_provider = models.CharField(max_length=30, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    UNIT_TYPE_CHOICES = [
        ("ft", "Linear Feet"),
        ("sqft", "Square Feet"),
        ("hour", "Hour"),
        ("item", "Per Item"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_type = models.CharField(
        max_length=20,
        choices=UNIT_TYPE_CHOICES,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (${self.unit_price}/{self.unit_type})"


class Quote(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent to Client"),
        ("viewed", "Viewed by Client"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("expired", "Expired"),
    ]

    TIME_PERIOD_CHOICES = [
        ("standard", "8am-5pm (Standard)"),
        ("evening", "5pm-2am (Evening Rate, +$500)"),
        ("weekend", "Weekend/Holiday (+$700)"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="quotes")
    title = models.CharField(max_length=200, default="Line Striping Quote")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(days=30)
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    time_period = models.CharField(
        max_length=20, choices=TIME_PERIOD_CHOICES, default="standard"
    )
    evening_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    weekend_fee = models.DecimalField(max_digits=10, decimal_places=2, default=700.00)
    number_of_days = models.IntegerField(default=1)

    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Access security
    access_token = models.CharField(max_length=32, unique=True, editable=False)
    verification_code = models.CharField(max_length=6, editable=False)

    notes = models.TextField(blank=True)
    job_location = models.TextField(blank=True)
    expected_completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Quote {self.id} for {self.client.name}"

    def save(self, *args, **kwargs):
        if not self.access_token:
            # Generate token on first save
            import random
            import secrets

            self.access_token = secrets.token_hex(16)
            self.verification_code = "".join(
                [str(random.randint(0, 9)) for _ in range(6)]
            )
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def time_period_fee(self):
        if self.time_period == "evening":
            return self.evening_fee
        elif self.time_period == "weekend":
            return self.weekend_fee
        return 0

    @property
    def discount_amount(self):
        return (self.subtotal * self.discount_percentage) / 100

    @property
    def total_amount(self):
        return self.subtotal + self.time_period_fee - self.discount_amount


class QuoteItem(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="items")
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.GeneratedField(
        expression=models.F("quantity") * models.F("unit_price"),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
    )

    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Set unit price from service if not specified
        if not self.unit_price:
            self.unit_price = self.service.default_price
        super().save(*args, **kwargs)


class Job(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    quote = models.OneToOneField(Quote, on_delete=models.CASCADE, related_name="job")
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    notes = models.TextField(blank=True)


class MaterialUsage(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="materials")
    material_type = models.CharField(
        max_length=100
    )  # e.g., "Yellow Paint", "White Paint"
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20)  # e.g., "gallon", "can"
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_recorded = models.DateTimeField(auto_now_add=True)


class TimeEntry(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="time_entries")
    staff = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="time_entries"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)

    @property
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return None


class JobPhoto(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="job_photos/")
    caption = models.CharField(max_length=200, blank=True)
    photo_type = models.CharField(
        max_length=20,
        choices=[("before", "Before"), ("during", "During Work"), ("after", "After")],
        default="during",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        "CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_photos",
    )
