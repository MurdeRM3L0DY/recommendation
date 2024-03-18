from django.contrib.auth import get_user_model

from rest_framework import serializers

from recommendation.movies.models import Movie

User = get_user_model()

class MoviesGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"

class MoviesPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "release_date", "streaming_platform"]


class MoviesRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    release_date = serializers.DateField()
    streaming_platform = serializers.ChoiceField(Movie.StreamingPlatforms.CHOICES)

class MoviesAuthGetSerializer(serializers.Serializer):
    movie = MoviesGetSerializer()
    watched = serializers.BooleanField()
