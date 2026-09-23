from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, ProfileSerializer


class RegisterView(generics.CreateAPIView):
    """Public endpoint — anyone can create an account."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    """Returns {access, refresh} tokens for username/password."""
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """Authenticated user's own profile — no username lookup needed."""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
