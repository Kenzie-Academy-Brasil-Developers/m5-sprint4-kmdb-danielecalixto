from rest_framework import serializers

from .models import Movie
from genres.models import Genre

from genres.serializers import GenreSerializer

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    duration = serializers.CharField()
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        for genre in genres_data:
            genre, created = Genre.objects.get_or_create(**genre)
            movie.genres.add(genre)
        return movie