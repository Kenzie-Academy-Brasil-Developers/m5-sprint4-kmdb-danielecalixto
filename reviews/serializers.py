from urllib import request
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Review, RecommendationType

from movies.models import Movie
from movies.serializers import MovieSerializer

from users.models import User
from users.serializers import UserSerializer


import ipdb

class ReviewSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Review
        fields = ['id', 'stars', 'review', 'spoilers', 'recommendation', 'movie_id']
        write_only_fields = ['movie', 'user']
        extra_kwargs = {'recommendation': {'required': False}, 'movie': {'required': False}, 'user': {'required': False}}
        read_only_fields = ['critic']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        recomm = instance.get_recommendation_display()
        user = User.objects.get(email=instance.user)
        critic = {}
        critic['id'] = user.id
        critic['first_name'] = user.first_name
        critic['last_name'] = user.last_name
        representation['critic'] = critic
        representation['recommendation'] = recomm
        return representation

    def validate_stars(self, value):
        if value>10:
            raise ValidationError("Ensure this value is less than or equal to 10.")
        elif value<1:
            raise ValidationError("Ensure this value is greater than or equal to 1.")
        return value
    
    def create(self, validated_data):
        movie_id = validated_data.pop('movie_id')
        movie = Movie.objects.get(pk=movie_id)
        user = validated_data.pop('user')
        review = Review.objects.create(movie=movie, user=user, **validated_data)
        return review