# WanderBook

A travel booking platform built with **Django 6** and **Tailwind CSS v4** (via [django-tailwind](https://github.com/timonweb/django-tailwind) standalone binary — Node.js not required).

Browse destinations, explore tour packages, book trips, and manage bookings from a polished web UI or JWT API.

**Live repo:** https://github.com/Praveenskg/django-tailwind

## Stack

| Layer | Tech |
|-------|------|
| Backend | Django 6, DRF, SimpleJWT |
| Frontend | Django templates, Tailwind CSS v4 |
| Admin | [Unfold](https://unfoldadmin.com/) |
| API docs | drf-spectacular (Swagger / ReDoc) |
| Animations | GSAP + ScrollTrigger |
| Icons | Heroicons (custom template tag) |
| CI | GitHub Actions |

## Requirements

- Python 3.11+
- pip

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py tailwind install   # first time only
python manage.py createsuperuser    # optional, for admin
```

Sample destinations and tour packages (Manali, Goa, Kerala, Rajasthan, Andaman) are loaded automatically via migrations.

## Development

Run Django and the Tailwind watcher together:

```bash
python manage.py tailwind dev
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Or run separately:

```bash
python manage.py runserver
python manage.py tailwind start
```

Hot reload is enabled via `django-browser-reload`.

## Pages

| URL | Description |
|-----|-------------|
| `/` | Home — hero, search, featured destinations, popular packages |
| `/explore/` | All destinations (search supported via `?q=`) |
| `/explore/<slug>/` | Destination detail + tour packages |
| `/trips/book/<pkg_id>/` | Book a package (login required) |
| `/trips/mine/` | My trips (login required) |
| `/dashboard/` | User dashboard (login required) |
| `/dashboard/profile/` | Edit profile & avatar |
| `/login/` | Sign in |
| `/signup/` | Create account |
| `/logout/` | Sign out |
| `/admin/` | Admin panel (Unfold) |

## Auth (web)

- Sign up at `/signup/` — redirects to dashboard after registration
- Sign in at `/login/`
- Profile avatar stored in `media/` (served in DEBUG mode)

## Travel booking

### Models

- **Destination** — name, slug, country, tagline, cover image URL, featured flag
- **TourPackage** — linked to destination, duration, price per person, max seats, highlights
- **Booking** — user, package, travel date, num travelers, total price (auto-calculated), status

### Admin

Manage everything under **Travel** in the Unfold sidebar:

- Destinations (inline packages, bulk featured/active actions)
- Tour packages (duplicate, activate/deactivate)
- Bookings (confirm, cancel, status badges)

## Auth API (JWT)

Interactive docs:

- Swagger UI: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- ReDoc: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- OpenAPI schema: [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

Base URL: `http://127.0.0.1:8000/api/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/api/auth/register/` | No | Create a user |
| `POST` | `/api/auth/login/` | No | Get access + refresh tokens |
| `POST` | `/api/auth/refresh/` | No | Refresh access token |
| `GET` | `/api/auth/me/` | Bearer | Current user profile |

### Register

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"StrongPass123!","password_confirm":"StrongPass123!"}'
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"StrongPass123!"}'
```

### Current user

```bash
curl http://127.0.0.1:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

## Bookings API

Base URL: `http://127.0.0.1:8000/api/bookings/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/bookings/destinations/` | No | List active destinations |
| `GET` | `/api/bookings/` | Bearer | List your bookings |
| `POST` | `/api/bookings/` | Bearer | Create a booking |
| `GET` | `/api/bookings/<id>/` | Bearer | Booking detail |
| `DELETE` | `/api/bookings/<id>/` | Bearer | Cancel booking (sets status) |

## CI

GitHub Actions runs on every push and pull request to `main`:

- `python manage.py check`
- Migrations apply + `--check`
- `python manage.py tailwind build`
- `python manage.py test`

Workflow: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

## Production

Build CSS and collect static files before deploying:

```bash
python manage.py tailwind build
python manage.py collectstatic
```

Use a production-ready database (PostgreSQL recommended), set `DEBUG=False`, configure `ALLOWED_HOSTS`, and move secrets to environment variables.

## Project structure

```
config/                 # Django settings & root URLs
api/                    # JWT auth API
bookings/               # Travel app (destinations, packages, bookings)
  models.py             # Destination, TourPackage, Booking
  templates/bookings/   # explore, detail, booking form, my trips
core/                   # Home, dashboard, auth, profile
  templatetags/         # heroicons template tag
  templates/core/       # home, dashboard, navbar partial
theme/                  # Tailwind CSS app
  static_src/src/styles.css   # Source CSS + design tokens
  static/css/dist/styles.css    # Compiled CSS
  static/js/gsap-animations.js  # GSAP scroll & hero animations
.github/workflows/      # CI pipeline
```

## Using Tailwind in templates

```html
{% load static tailwind_tags %}
{% tailwind_css %}

<h1 class="text-4xl font-bold text-sky-700">Hello Tailwind</h1>
```

## Using Heroicons

```html
{% load heroicons %}
{% heroicon "paper-airplane" "h-5 w-5 text-sky-500" %}
```

Available icons are defined in `core/templatetags/heroicons.py`.
