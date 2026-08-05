from django.db import migrations


def create_sample_services(apps, schema_editor):
    Service = apps.get_model("bookings", "Service")
    samples = [
        {
            "name": "Strategy call",
            "description": "30-minute consultation to plan your product or roadmap.",
            "duration_minutes": 30,
            "price": "999.00",
        },
        {
            "name": "Design review",
            "description": "Walk through your UI and get actionable feedback.",
            "duration_minutes": 45,
            "price": "1499.00",
        },
        {
            "name": "Onboarding session",
            "description": "Full setup walkthrough for your team and workflows.",
            "duration_minutes": 60,
            "price": "2499.00",
        },
    ]
    for item in samples:
        Service.objects.get_or_create(name=item["name"], defaults=item)


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_sample_services, migrations.RunPython.noop),
    ]
