from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import LoginSerializer


class AuthViewSet(viewsets.ViewSet):
    """
    /api/auth/login/  (POST) -> token
    /api/auth/me/     (GET)  -> current user info
    """

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        # For demo: use email-as-username (admin sets username to email)
        username = s.validated_data["username"]
        password = s.validated_data["password"]

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    @action(detail=False, methods=["get"])
    def me(self, request):
        u = request.user
        return Response({"id": u.id, "username": u.username, "email": u.email})