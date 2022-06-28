from django.forms import ValidationError
from rest_framework import serializers
from .models import Review

from movies.models import Movie

from users.models import User


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'stars', 'review', 'spoilers', 'recommendation', 'movie_id', 'critic']
        extra_kwargs = {'recommendation': {'required': False}, 'movie': {'required': False}, 'critic': {'required': False}}

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     recomm = instance.get_recommendation_display()
    #     representation['recommendation'] = recomm
    #     return representation

    def validate_stars(self, value):
        if value>10:
            raise ValidationError("Ensure this value is less than or equal to 10.")
        elif value<1:
            raise ValidationError("Ensure this value is greater than or equal to 1.")
        return value
    
    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        critic = validated_data.pop('critic')
        review = Review.objects.create(movie=movie, critic=critic, **validated_data)
        return review