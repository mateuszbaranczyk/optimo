from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UserModel

from .serializers import LoginSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]

    model = get_user_model()
    serializer_class = UserSerializer


class LoginUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        user = self._authenticate(request)

        if user:
            response_data = self._create_response_with_token(user)
            return Response(response_data, status=HTTP_200_OK)
        return Response(
            status=HTTP_401_UNAUTHORIZED,
        )

    def _authenticate(self, request: Request) -> AbstractUser | None:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(
                username=serializer.data["username"],
                password=serializer.data["password"],
            )
            return user
        return None

    def _create_response_with_token(self, user: AbstractUser) -> dict:
        refresh = RefreshToken.for_user(user)
        response_data = {
            "user": UserSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return response_data
