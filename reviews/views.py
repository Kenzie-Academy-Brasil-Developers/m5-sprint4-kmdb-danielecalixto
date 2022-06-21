from django.shortcuts import render
from rest_framework.views import APIView, Response, status

from .models import Review
from .serializers import ReviewSerializer

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated  


class ReviewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        pass

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except AttributeError as err:
            if err.args[1]==False:
                return Response(
                    {"stars": "Ensure this value is an integer."},
                    status.HTTP_400_BAD_REQUEST
                    )
            elif err.args[0]>10:
                return Response(
                    {"stars": "Ensure this value is less than or equal to 10."},
                    status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"stars": "Ensure this value is greater than or equal to 1."},
                    status.HTTP_400_BAD_REQUEST
                    )


class ReviewViewDetail(APIView):

    def delete(self, request, review_id):
        pass

class AllReviewsView(APIView):
    def get(self, request):
        pass