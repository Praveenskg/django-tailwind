from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import BookingForm
from .models import Booking, Destination, TourPackage


def destinations_view(request):
    query = request.GET.get("q", "").strip()
    destinations = Destination.objects.filter(is_active=True)
    if query:
        destinations = destinations.filter(name__icontains=query)
    featured = destinations.filter(is_featured=True)
    rest = destinations.filter(is_featured=False)
    return render(request, "bookings/destinations.html", {
        "destinations": destinations,
        "featured": featured,
        "rest": rest,
        "query": query,
    })


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug, is_active=True)
    packages = destination.packages.filter(is_active=True)
    return render(request, "bookings/destination_detail.html", {
        "destination": destination,
        "packages": packages,
    })


@login_required
@require_http_methods(["GET", "POST"])
def book_package(request, pkg_id):
    package = get_object_or_404(TourPackage, pk=pkg_id, is_active=True)
    form = BookingForm(request.POST or None, initial={"package": package})
    if request.method == "POST" and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.package = package
        booking.save()
        messages.success(
            request,
            f"Trip booked! {package.name} on {booking.travel_date:%b %d, %Y} for {booking.num_travelers} traveler(s).",
        )
        return redirect("my_trips")
    return render(request, "bookings/booking_form.html", {"form": form, "package": package})


@login_required
def my_trips(request):
    bookings = (
        Booking.objects
        .filter(user=request.user)
        .select_related("package", "package__destination")
    )
    return render(request, "bookings/my_trips.html", {"bookings": bookings})


@login_required
@require_http_methods(["POST"])
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status != Booking.Status.CANCELLED:
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status"])
        messages.success(request, f"Trip to {booking.package.destination.name} has been cancelled.")
    else:
        messages.info(request, "This trip was already cancelled.")
    return redirect("my_trips")
