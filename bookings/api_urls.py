from django.urls import path

from .serializers import BookingDetailView, BookingListCreateView, DestinationListView

urlpatterns = [
    path("destinations/", DestinationListView.as_view(), name="api-destinations"),
    path("", BookingListCreateView.as_view(), name="api-bookings"),
    path("<int:pk>/", BookingDetailView.as_view(), name="api-booking-detail"),
]
