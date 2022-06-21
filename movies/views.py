from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Response, status

from .models import Movie
from .serializers import MovieSerializer

from rest_framework.authentication import TokenAuthentication

from .permissions import AdminPermission

class MovieView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]

    def get(self, _):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

class MovieViewDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AdminPermission]
    
    def get(self, resquest, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def patch(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(movie, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)