from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import APIKey
from .serializers import RegisterSerializer, UserSerializer, RoleTokenSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = RoleTokenSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class ApiKeyCreateView(APIView):
    """Logged-in user generates an API key for the custom scheme."""
    def post(self, request):
        key = APIKey.objects.create(user=request.user)
        return Response({"api_key": key.key}, status=201)