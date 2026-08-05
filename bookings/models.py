from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Destination(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    country = models.CharField(max_length=80)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    cover_image_url = models.URLField(
        blank=True,
        help_text="Unsplash or any public image URL",
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-is_featured", "name")

    def __str__(self):
        return f"{self.name}, {self.country}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourPackage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="packages",
    )
    name = models.CharField(max_length=120)
    duration_days = models.PositiveIntegerField(default=3)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    max_seats = models.PositiveIntegerField(default=20)
    highlights = models.TextField(
        blank=True,
        help_text="One highlight per line",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("price_per_person",)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"

    @property
    def highlights_list(self):
        return [h.strip() for h in self.highlights.splitlines() if h.strip()]

    @property
    def duration_nights(self):
        return max(self.duration_days - 1, 0)


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    package = models.ForeignKey(
        TourPackage,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    travel_date = models.DateField()
    num_travelers = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("travel_date",)

    def __str__(self):
        return f"{self.package.name} · {self.travel_date} × {self.num_travelers}"

    def save(self, *args, **kwargs):
        if self.package_id and self.num_travelers:
            self.total_price = self.package.price_per_person * self.num_travelers
        super().save(*args, **kwargs)
