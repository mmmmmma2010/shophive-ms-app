from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterationSerializer, ProfileSerializer
import logging
from .models import User

logger = logging.getLogger(__name__)


class RegisterationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info(f"User registered successfully: {user.email}")

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "status": "success",
                "message": "User registered successfully",
                "data": {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(request, username=email, password=password)
    if user is None:
        return Response(
            {
                "status": "error",
                "message": "Invalid credentials",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "status": "success",
            "message": "User logged in successfully",
            "data": {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
        },
        status=status.HTTP_200_OK,
    )


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        user_id = self.request.META.get("HTTP_X_USER_ID")
        return User.objects.get(id=user_id)
