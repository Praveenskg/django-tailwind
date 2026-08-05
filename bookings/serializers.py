from rest_framework import generics, permissions, serializers

from .models import Booking, Destination, TourPackage


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ("id", "name", "slug", "country", "tagline", "cover_image_url", "is_featured")


class TourPackageSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source="destination.name", read_only=True)

    class Meta:
        model = TourPackage
        fields = (
            "id", "destination", "destination_name", "name",
            "duration_days", "price_per_person", "max_seats", "highlights",
        )


class BookingSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source="package.name", read_only=True)
    destination_name = serializers.CharField(source="package.destination.name", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id", "package", "package_name", "destination_name",
            "travel_date", "num_travelers", "total_price",
            "status", "notes", "created_at",
        )
        read_only_fields = ("total_price", "status", "created_at")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return Booking.objects.create(**validated_data)


class DestinationListView(generics.ListAPIView):
    queryset = Destination.objects.filter(is_active=True)
    serializer_class = DestinationSerializer
    permission_classes = [permissions.AllowAny]


class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            "package", "package__destination"
        )


class BookingDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related(
            "package", "package__destination"
        )

    def perform_destroy(self, instance):
        instance.status = Booking.Status.CANCELLED
        instance.save(update_fields=["status"])
