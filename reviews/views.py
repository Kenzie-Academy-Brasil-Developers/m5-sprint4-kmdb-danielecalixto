from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView, Response, status

from .models import Review
from .serializers import ReviewSerializer

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated  

from .permissions import ListPermission

import ipdb

class ReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ListPermission]

    def get(self, _, movie_id):
        reviews = Review.objects.all()
        reviews.filter(movie_id=movie_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, movie_id):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=request.user, movie_id=movie_id)
        except ValidationError as err:
            return Response(err.message, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status.HTTP_201_CREATED)

class ReviewViewDetail(APIView):
    def delete(self, request, review_id):
        pass

class AllReviewsView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)