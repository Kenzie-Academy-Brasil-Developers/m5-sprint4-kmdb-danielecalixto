from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserSerializer, LoginSerializer
from users import serializers

class UserView(APIView):
    def get(self, _):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

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
