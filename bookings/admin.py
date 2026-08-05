from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import action, display

from .models import Booking, Destination, TourPackage


class TourPackageInline(TabularInline):
    model = TourPackage
    extra = 1
    fields = ("name", "duration_days", "price_per_person", "max_seats", "is_active")
    show_change_link = True


@admin.register(Destination)
class DestinationAdmin(ModelAdmin):
    list_display = (
        "show_cover",
        "name",
        "country",
        "package_count",
        "is_featured",
        "is_active",
        "created_at",
    )
    list_filter = ("is_featured", "is_active", "country")
    list_editable = ("is_featured", "is_active")
    search_fields = ("name", "country", "tagline", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "show_cover_preview")
    inlines = [TourPackageInline]
    actions = ["mark_featured", "unmark_featured", "activate_destinations", "deactivate_destinations"]

    fieldsets = (
        (None, {
            "fields": ("name", "slug", "country", "tagline", "is_featured", "is_active"),
        }),
        ("Content", {
            "fields": ("description", "cover_image_url", "show_cover_preview"),
        }),
        ("Meta", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _package_count=Count("packages"),
        )

    @display(description="Cover", image=True)
    def show_cover(self, obj):
        if obj.cover_image_url:
            return obj.cover_image_url
        return None

    @display(description="Preview")
    def show_cover_preview(self, obj):
        if obj.cover_image_url:
            return format_html(
                '<img src="{}" style="max-width:320px;max-height:180px;border-radius:8px;object-fit:cover;" />',
                obj.cover_image_url,
            )
        return "—"

    @display(description="Packages")
    def package_count(self, obj):
        return obj._package_count

    @action(description="Mark as featured")
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} destination(s) marked as featured.", messages.SUCCESS)

    @action(description="Remove featured")
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} destination(s) unmarked.", messages.SUCCESS)

    @action(description="Activate selected")
    def activate_destinations(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} destination(s) activated.", messages.SUCCESS)

    @action(description="Deactivate selected")
    def deactivate_destinations(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} destination(s) deactivated.", messages.SUCCESS)


@admin.register(TourPackage)
class TourPackageAdmin(ModelAdmin):
    list_display = (
        "name",
        "destination",
        "show_duration",
        "price_per_person",
        "max_seats",
        "booking_count",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "destination", "duration_days")
    list_editable = ("is_active",)
    search_fields = ("name", "destination__name", "highlights")
    autocomplete_fields = ("destination",)
    readonly_fields = ("created_at", "booking_count_readonly")
    actions = [
        "activate_packages",
        "deactivate_packages",
        "duplicate_packages",
    ]

    fieldsets = (
        (None, {
            "fields": ("destination", "name", "is_active"),
        }),
        ("Pricing & capacity", {
            "fields": ("duration_days", "price_per_person", "max_seats"),
        }),
        ("Details", {
            "fields": ("highlights",),
            "description": "Enter one highlight per line. These appear on the destination detail page.",
        }),
        ("Stats", {
            "fields": ("booking_count_readonly", "created_at"),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("destination").annotate(
            _booking_count=Count("bookings"),
        )

    @display(description="Duration")
    def show_duration(self, obj):
        nights = max(obj.duration_days - 1, 0)
        return f"{obj.duration_days}D / {nights}N"

    @display(description="Bookings")
    def booking_count(self, obj):
        return obj._booking_count

    @display(description="Total bookings")
    def booking_count_readonly(self, obj):
        if obj.pk:
            return obj.bookings.count()
        return "—"

    @action(description="Activate selected packages")
    def activate_packages(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} package(s) activated.", messages.SUCCESS)

    @action(description="Deactivate selected packages")
    def deactivate_packages(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} package(s) deactivated.", messages.SUCCESS)

    @action(description="Duplicate selected packages")
    def duplicate_packages(self, request, queryset):
        count = 0
        for pkg in queryset:
            pkg.pk = None
            pkg.name = f"{pkg.name} (copy)"
            pkg.is_active = False
            pkg.save()
            count += 1
        self.message_user(request, f"{count} package(s) duplicated as drafts.", messages.SUCCESS)


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = (
        "show_trip",
        "user",
        "travel_date",
        "num_travelers",
        "total_price",
        "show_status",
        "created_at",
    )
    list_filter = ("status", "travel_date", "package__destination")
    search_fields = (
        "user__username",
        "user__email",
        "package__name",
        "package__destination__name",
        "notes",
    )
    autocomplete_fields = ("user", "package")
    readonly_fields = ("total_price", "created_at")
    date_hierarchy = "travel_date"
    actions = ["confirm_bookings", "cancel_bookings", "mark_pending"]

    fieldsets = (
        (None, {
            "fields": ("user", "package", "status"),
        }),
        ("Trip details", {
            "fields": ("travel_date", "num_travelers", "total_price", "notes"),
        }),
        ("Meta", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "user", "package", "package__destination",
        )

    @display(description="Trip", header=True)
    def show_trip(self, obj):
        return [
            obj.package.name,
            obj.package.destination.name,
            obj.package.destination.name[0].upper(),
        ]

    @display(
        description="Status",
        label={
            "confirmed": "success",
            "pending": "warning",
            "cancelled": "danger",
        },
    )
    def show_status(self, obj):
        return obj.status, obj.get_status_display()

    @action(description="Confirm selected bookings")
    def confirm_bookings(self, request, queryset):
        updated = queryset.exclude(status=Booking.Status.CANCELLED).update(
            status=Booking.Status.CONFIRMED,
        )
        self.message_user(request, f"{updated} booking(s) confirmed.", messages.SUCCESS)

    @action(description="Cancel selected bookings")
    def cancel_bookings(self, request, queryset):
        updated = queryset.update(status=Booking.Status.CANCELLED)
        self.message_user(request, f"{updated} booking(s) cancelled.", messages.SUCCESS)

    @action(description="Mark as pending")
    def mark_pending(self, request, queryset):
        updated = queryset.exclude(status=Booking.Status.CANCELLED).update(
            status=Booking.Status.PENDING,
        )
        self.message_user(request, f"{updated} booking(s) marked pending.", messages.SUCCESS)
