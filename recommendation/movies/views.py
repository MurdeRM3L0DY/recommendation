# FIXME: Use a Serializer wherever possible

from django.contrib.auth import get_user_model

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework.exceptions import APIException, NotAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from recommendation.movies.serializers import (
    MoviesAuthGetSerializer,
    MoviesRequestSerializer,
    MoviesGetSerializer,
)
from recommendation.movies.models import Movie
from recommendation.watchlist.models import WatchList

User = get_user_model()


# Create your views here.
class MoviesViewSet(GenericViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return MoviesRequestSerializer

        if self.action == "list":
            return MoviesGetSerializer

        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="streaming_platform",
                type=OpenApiTypes.STR,
                required=False,
            ),
            OpenApiParameter(
                name="watched",
                type=OpenApiTypes.BOOL,
                required=False,
            ),
        ],
        # override default docstring extraction
        description="",
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
    )
    def list(self, request: Request):
        queryset = self.queryset
        streaming_platform = request.query_params.get("streaming_platform")

        # optionally filter by streaming_platform
        if streaming_platform:
            queryset = queryset.filter(streaming_platform=streaming_platform)

        if not request.user.is_authenticated:
            serializer = MoviesGetSerializer(queryset, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            recommended_movies = []

            # parse `watched` query param
            watched_bool_str = request.query_params.get("watched")
            watched_bool = False
            if watched_bool_str:
                watched_bool = watched_bool_str.lower() in ["true", "1"]

            user_watchlist = WatchList.objects.filter(user=request.user)
            friends_watchlist = WatchList.objects.filter(
                user__in=request.user.friends.all()
            ).exclude(movie__in=user_watchlist.values("movie"))
            if streaming_platform:
                user_watchlist = user_watchlist.filter(
                    movie__streaming_platform=streaming_platform
                )
                friends_watchlist = friends_watchlist.filter(
                    movie__streaming_platform=streaming_platform
                )

            # ALL movie ids NOT IN user and friends watchlist
            #
            # this has to be calculated before filtering user_watchlist
            # on the `watched` query param
            #
            # rest_movie_ids = queryset.values("id").difference(
            #     user_watchlist.values("movie"), friends_watchlist.values("movie")
            # )
            rest_movie_ids = (
                queryset.values("id")
                .exclude(
                    id__in=user_watchlist.values("movie"),
                )
                .exclude(id__in=friends_watchlist.values("movie"))
            )

            if watched_bool_str:
                user_watchlist = user_watchlist.filter(watched=watched_bool)

            # movies in friends watchlist
            for wl in friends_watchlist:
                if (watched_bool_str and not watched_bool) or not watched_bool_str:
                    recommended_movies.append({"movie": wl.movie, "watched": False})

            # movies not in user watchlist
            for movie in queryset.filter(id__in=rest_movie_ids):
                if (watched_bool_str and not watched_bool) or not watched_bool_str:
                    recommended_movies.append({"movie": movie, "watched": False})

            # finally, movies in user watchlist
            for wl in user_watchlist:
                recommended_movies.append({"movie": wl.movie, "watched": wl.watched})

            serializer = MoviesAuthGetSerializer(recommended_movies, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        # override default docstring extraction
        description="",
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
    )
    def create(self, request: Request):
        if request.user.is_authenticated:
            serializer = MoviesRequestSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data

                title = data.get("title")
                release_date = data.get("release_date")
                streaming_platform = data.get("streaming_platform")

                new_movie, created = self.queryset.get_or_create(
                    title=title,
                    release_date=release_date,
                    streaming_platform=streaming_platform,
                )
                if not created:
                    raise APIException("movie already exists", status.HTTP_409_CONFLICT)

                serializer = MoviesGetSerializer(new_movie)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated()
