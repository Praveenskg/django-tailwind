from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from bookings.models import Booking, Destination, TourPackage
from .forms import ProfileForm, SignupForm
from .models import Profile


def home(request):
    featured_destinations = Destination.objects.filter(is_active=True, is_featured=True)[:3]
    popular_packages = TourPackage.objects.filter(is_active=True).select_related("destination")[:6]
    return render(request, "core/home.html", {
        "featured_destinations": featured_destinations,
        "popular_packages": popular_packages,
    })


@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    now = timezone.now()
    user_bookings = Booking.objects.filter(user=request.user).select_related(
        "package", "package__destination"
    )
    upcoming_bookings = user_bookings.filter(
        travel_date__gte=now.date(),
        status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED],
    ).order_by("travel_date")[:5]

    context = {
        "profile": profile,
        "stats": {
            "upcoming": upcoming_bookings.count(),
            "total": user_bookings.count(),
            "destinations": Destination.objects.filter(is_active=True).count(),
        },
        "upcoming_bookings": upcoming_bookings,
    }
    return render(request, "core/dashboard.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,
        user=request.user,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("dashboard")
    return render(request, "core/profile.html", {"form": form, "profile": profile})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect("dashboard")

    return render(
        request,
        "core/login.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@require_http_methods(["GET", "POST"])
def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")

    return render(request, "core/signup.html", {"form": form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect("login")
