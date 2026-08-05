"""
Replace Service + old Booking with Destination, TourPackage, new Booking.
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_sample_services"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1. Drop old Booking first (FK to Service)
        migrations.DeleteModel(name="Booking"),
        # 2. Drop old Service
        migrations.DeleteModel(name="Service"),
        # 3. Create Destination
        migrations.CreateModel(
            name="Destination",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(max_length=140, unique=True, blank=True)),
                ("country", models.CharField(max_length=80)),
                ("tagline", models.CharField(max_length=200, blank=True)),
                ("description", models.TextField(blank=True)),
                ("cover_image_url", models.URLField(blank=True, help_text="Unsplash or any public image URL")),
                ("is_featured", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-is_featured", "name")},
        ),
        # 4. Create TourPackage
        migrations.CreateModel(
            name="TourPackage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("destination", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="packages", to="bookings.destination")),
                ("name", models.CharField(max_length=120)),
                ("duration_days", models.PositiveIntegerField(default=3)),
                ("price_per_person", models.DecimalField(max_digits=10, decimal_places=2)),
                ("max_seats", models.PositiveIntegerField(default=20)),
                ("highlights", models.TextField(blank=True, help_text="One highlight per line")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("price_per_person",)},
        ),
        # 5. Create new Booking
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bookings", to=settings.AUTH_USER_MODEL)),
                ("package", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="bookings", to="bookings.tourpackage")),
                ("travel_date", models.DateField()),
                ("num_travelers", models.PositiveIntegerField(default=1)),
                ("total_price", models.DecimalField(max_digits=12, decimal_places=2, default=0)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")], default="pending", max_length=20)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("travel_date",)},
        ),
    ]
