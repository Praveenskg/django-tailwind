from django.db import migrations


DESTINATIONS = [
    {
        "name": "Manali",
        "slug": "manali",
        "country": "India",
        "tagline": "Snow-capped peaks & mountain magic",
        "description": (
            "Manali is a high-altitude Himalayan resort town in India's northern Himachal Pradesh state. "
            "It's a gateway for skiing in the Solang Valley and trekking in Parvati Valley."
        ),
        "cover_image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=1800&q=80",
        "is_featured": True,
        "packages": [
            {
                "name": "Manali Adventure Escape — 4N5D",
                "duration_days": 5,
                "price_per_person": "12999.00",
                "max_seats": 15,
                "highlights": "Solang Valley snow activities\nRohtang Pass excursion\nOld Manali café hopping\nHadimba Temple visit\nBeas River riverside camp",
            },
            {
                "name": "Manali Honeymoon Special — 3N4D",
                "duration_days": 4,
                "price_per_person": "18999.00",
                "max_seats": 8,
                "highlights": "Luxury valley-view resort\nPrivate candlelight dinner\nCouple spa session\nSunrise trek to Jogini Falls\nApple orchard walk",
            },
        ],
    },
    {
        "name": "Goa",
        "slug": "goa",
        "country": "India",
        "tagline": "Sun, sand & endless sunsets",
        "description": (
            "Goa is a state on the southwestern coast of India within the Konkan region. "
            "It is bounded by the state of Maharashtra to the north and Karnataka to the east and south."
        ),
        "cover_image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=1800&q=80",
        "is_featured": True,
        "packages": [
            {
                "name": "Goa Beach Party — 3N4D",
                "duration_days": 4,
                "price_per_person": "9999.00",
                "max_seats": 25,
                "highlights": "North Goa beaches — Baga, Calangute\nNightlife at Tito's Lane\nDudhsagar Waterfalls day trip\nCasino cruise on Mandovi River\nSpice plantation tour",
            },
            {
                "name": "Goa Heritage Explorer — 5N6D",
                "duration_days": 6,
                "price_per_person": "14499.00",
                "max_seats": 18,
                "highlights": "Old Goa churches & basilicas\nPanjim Latin Quarter walk\nSouth Goa secluded beaches\nSeafood culinary tour\nSunset yoga on Palolem beach",
            },
        ],
    },
    {
        "name": "Kerala",
        "slug": "kerala",
        "country": "India",
        "tagline": "God's own country — backwaters & spice",
        "description": (
            "Kerala, a state on India's tropical Malabar Coast, has nearly 600 km of Arabian Sea shoreline. "
            "It's known for its palm-lined beaches and backwaters."
        ),
        "cover_image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=1800&q=80",
        "is_featured": True,
        "packages": [
            {
                "name": "Kerala Backwaters & Munnar — 5N6D",
                "duration_days": 6,
                "price_per_person": "16999.00",
                "max_seats": 20,
                "highlights": "Alleppey houseboat overnight stay\nMunnar tea garden trek\nPeriyar wildlife sanctuary\nKochi Fort & Jewish Town walk\nAyurvedic wellness session",
            },
        ],
    },
    {
        "name": "Rajasthan",
        "slug": "rajasthan",
        "country": "India",
        "tagline": "Royal forts, desert dunes & vivid colors",
        "description": (
            "Rajasthan is India's largest state by area. Known as the Land of Kings, it evokes old-world splendour "
            "with its majestic forts, painted havelis and royal palaces."
        ),
        "cover_image_url": "https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=1800&q=80",
        "is_featured": False,
        "packages": [
            {
                "name": "Royal Rajasthan Circuit — 7N8D",
                "duration_days": 8,
                "price_per_person": "22999.00",
                "max_seats": 20,
                "highlights": "Jaipur Amber Fort & City Palace\nJodhpur Blue City walk\nJaisalmer desert safari & camp\nUdaipur lake palace sunset cruise\nPushkar camel fair (seasonal)",
            },
        ],
    },
    {
        "name": "Andaman Islands",
        "slug": "andaman",
        "country": "India",
        "tagline": "Crystal waters & coral reefs",
        "description": (
            "The Andaman Islands are an Indian archipelago in the Bay of Bengal. "
            "These roughly 300 islands have palm-lined, white-sand beaches, mangroves and tropical rainforests."
        ),
        "cover_image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1800&q=80",
        "is_featured": False,
        "packages": [
            {
                "name": "Andaman Island Hopper — 5N6D",
                "duration_days": 6,
                "price_per_person": "27999.00",
                "max_seats": 12,
                "highlights": "Radhanagar Beach — Asia's best beach\nScuba diving at Elephant Beach\nCellular Jail sound & light show\nRoss Island & North Bay snorkelling\nGlass-bottom boat ride",
            },
        ],
    },
]


def create_sample_data(apps, schema_editor):
    Destination = apps.get_model("bookings", "Destination")
    TourPackage = apps.get_model("bookings", "TourPackage")

    for dest_data in DESTINATIONS:
        packages = dest_data.pop("packages")
        dest, _ = Destination.objects.get_or_create(
            slug=dest_data["slug"],
            defaults=dest_data,
        )
        for pkg_data in packages:
            TourPackage.objects.get_or_create(
                destination=dest,
                name=pkg_data["name"],
                defaults=pkg_data,
            )


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0003_travel_models"),
    ]

    operations = [
        migrations.RunPython(create_sample_data, migrations.RunPython.noop),
    ]
