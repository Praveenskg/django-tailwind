from django.urls import path

from . import views

urlpatterns = [
    path("explore/", views.destinations_view, name="destinations"),
    path("explore/<slug:slug>/", views.destination_detail, name="destination_detail"),
    path("trips/book/<int:pkg_id>/", views.book_package, name="book_package"),
    path("trips/mine/", views.my_trips, name="my_trips"),
    path("trips/<int:pk>/cancel/", views.cancel_booking, name="cancel_booking"),
]
