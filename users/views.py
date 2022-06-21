from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .permissions import AdminPermission

from .models import User
from .serializers import UserSerializer, LoginSerializer
from users import serializers

class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]

    def get(self, _):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class UserViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username = serializer.validated_data['email'],
            password = serializer.validated_data['password']
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(
            {"detail": "Invalid email or password"}, status.HTTP_401_UNAUTHORIZED
        )
