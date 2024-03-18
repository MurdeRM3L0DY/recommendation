from rest_framework import serializers
from recommendation.movies.serializers import MoviesGetSerializer
from recommendation.watchlist.models import WatchList


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"

class WatchListRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ["watched"]

class WatchListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ["movie"]

class WatchedRetrieveSerializer(serializers.ModelSerializer):
    movie = MoviesGetSerializer

    class Meta:
        model = WatchList
        fields = ["id", "movie", "watched"]
