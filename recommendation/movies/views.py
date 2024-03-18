# FIXME: Use a Serializer wherever possible

from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import APIException
from rest_framework.viewsets import GenericViewSet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter

from recommendation.movies.serializers import MoviesAuthGetSerializer, MoviesRequestSerializer, MoviesGetSerializer
from recommendation.movies.models import Movie
from recommendation.users.models import Profile
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
        description='',
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

        if streaming_platform:
            queryset = queryset.filter(streaming_platform=streaming_platform)

        if not request.user.is_authenticated:
            serializer = MoviesGetSerializer(queryset, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            watched_bool_str = request.query_params.get("watched")
            watched_bool = False
            if watched_bool_str:
                watched_bool = watched_bool_str.lower() in ['true', '1']

            user_profile = Profile.objects.get(user=request.user)

            recommended_movies = []

            def append_recommended_movies(movie: Movie, wl: WatchList):
                recommended_movie = None

                if watched_bool_str is not None:
                    if wl:
                        if wl.watched == watched_bool:
                            recommended_movie = { "movie": movie, "watched": wl.watched == watched_bool}
                    else:
                        if watched_bool == False:
                            recommended_movie = { "movie": movie, "watched": False }
                else:
                    recommended_movie = { "movie": movie, "watched": bool(wl and wl.watched) }

                if recommended_movie and recommended_movie not in recommended_movies:
                    recommended_movies.append(recommended_movie)


            # push friends watchlist movies to the top of the list
            for friend in user_profile.friends.all():
                friend_watchlist = friend.watchlist.all()

                if streaming_platform:
                    friend_watchlist = friend_watchlist.filter(movie__streaming_platform=streaming_platform)

                for e in friend_watchlist:
                    user_watchlist = user_profile.watchlist.filter(movie=e.movie).first()
                    append_recommended_movies(e.movie, user_watchlist)


            # push the rest
            for movie in queryset:
                user_watchlist = user_profile.watchlist.filter(movie=movie).first()
                append_recommended_movies(movie, user_watchlist)


            serializer = MoviesAuthGetSerializer(recommended_movies, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

    @extend_schema(
        # override default docstring extraction
        description='',
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
    )
    def create(self, request: Request):
        serializer = MoviesRequestSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            title = data.get('title')
            release_date = data.get('release_date')
            streaming_platform = data.get('streaming_platform')

            if Movie.objects.filter(title=title).exists():
                raise APIException("movie already exists", status.HTTP_409_CONFLICT)

            new_movie = Movie.objects.create(
                title=title,
                release_date=release_date,
                streaming_platform=streaming_platform
            )
            new_movie.save()

            serializer = MoviesGetSerializer(new_movie)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
