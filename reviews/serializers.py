from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from .models import Review

from movies.models import Movie

import ipdb

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['stars', 'review', 'spoilers']
        extra_kwargs = {'recommendation': {'required': False}}
        read_only_fields = ['id', 'spoilers', 'movie_id', 'critic']

        def validate_stars(self, value):
            valid_int = isinstance(value, int)
            if valid_int==False or value<1 or value>10:
                raise AttributeError(value, valid_int)
    
        def create(self, validated_data):
            critic = CurrentUserDefault()
            movie_id = self.context['request'].query_params.get('movie_id')
            print(critic)
            print(movie_id)
            review = Review.objects.create(movie_id=movie_id, critic_id=critic.id, **validated_data)
            return review