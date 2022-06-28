from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response, status

from .models import Review
from .serializers import ReviewSerializer

from rest_framework.pagination import PageNumberPagination

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated  

from .permissions import ListPermission, DeletePermission

import ipdb

class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ListPermission]

    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        result_page = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, movie_id):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(critic=request.user, movie_id=movie_id)
        except ValidationError as err:
            return Response(err.message, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status.HTTP_201_CREATED)

class ReviewViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [DeletePermission]

    def delete(self, request, review_id):
        review = get_object_or_404(Review, pk=review_id)
        if review.user != request.user:
            return Response({"detail": "You do not have permission to perform this action."}, status.HTTP_403_FORBIDDEN)      
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AllReviewsView(APIView, PageNumberPagination):
    def get(self, request):
        reviews = Review.objects.all()
        result_page = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)