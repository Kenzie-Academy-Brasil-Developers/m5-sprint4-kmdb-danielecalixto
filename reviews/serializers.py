from urllib import request
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Review

from movies.models import Movie

import ipdb

class StarError(Exception):
    pass

class ReviewSerializer(serializers.ModelSerializer):
    movie_id = serializers.SerializerMethodField()
    critic_id = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['stars', 'review', 'spoilers']
        extra_kwargs = {'recommendation': {'required': False}, 'movie_id': {'required': False}, 'critic_id': {'required': False}}
        read_only_fields = ['id']

    def validate_stars(self, value):
        if value<1 or value>10:
            raise StarError(value)
        return value
    
    def get_movie_id(self, obj):
        movie_id = self.context['request'].query_params.get('movie_id')
        return movie_id

    def get_critic_id(self, obj):
        critic_id = self.context['request'].user
        return critic_id.id

    def create(self, validated_data):
        validated_data['movie_id'] = self['movie_id']
        validated_data['critic_id'] = self['critic_id']
        review = Review.objects.create(**validated_data)
        return review