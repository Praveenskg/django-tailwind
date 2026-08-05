from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Register a new user",
        description="Create an account with username, email, and password.",
    )
)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Login",
        description="Exchange username and password for JWT access and refresh tokens.",
    )
)
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=["Auth"],
        summary="Refresh access token",
        description="Get a new access token using a valid refresh token.",
    )
)
class RefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


@extend_schema_view(
    get=extend_schema(
        tags=["Auth"],
        summary="Current user",
        description="Return the authenticated user's profile.",
        responses={200: UserSerializer},
    )
)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
