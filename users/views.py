from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status

from .models import User
from .serializers import UserSerializer

class UserView(APIView):  

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)   
