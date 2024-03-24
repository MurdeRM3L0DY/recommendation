from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import APIException, NotAuthenticated, PermissionDenied
from rest_framework.request import Request

# from rest_framework.mixins import UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from recommendation.users.models import Profile

from recommendation.watchlist.models import WatchList
from recommendation.watchlist.serializers import (
    WatchListCreateSerializer,
    WatchListRequestSerializer,
    WatchListSerializer,
    WatchedRetrieveSerializer,
)


class WatchListViewSet(GenericViewSet):
    queryset = WatchList.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return WatchListCreateSerializer

        if self.action == "partial_update":
            return WatchListRequestSerializer

        return super().get_serializer_class()

    def list(self, request: Request):
        if request.user.is_authenticated:
            curr_profile = Profile.objects.get(user=request.user)
            serializer = WatchListSerializer(
                self.queryset.filter(profile=curr_profile), many=True
            )
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            raise NotAuthenticated()

    def create(self, request):
        if request.user.is_authenticated:
            serializer = WatchListCreateSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data

                movie = data.get("movie")

                if movie:
                    curr_profile = Profile.objects.get(user=request.user)

                    new_watched, created = self.queryset.get_or_create(
                        profile=curr_profile,
                        movie=movie,
                    )
                    if not created:
                        raise APIException(
                            "movie already added to watchlist",
                            status.HTTP_400_BAD_REQUEST,
                        )

                    serializer = WatchedRetrieveSerializer(new_watched)
                    return Response(serializer.data, status.HTTP_201_CREATED)
                else:
                    raise APIException("invalid movie_id", status.HTTP_400_BAD_REQUEST)

            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated()

    @extend_schema(
        request=WatchListRequestSerializer,
        # override default docstring extraction
        description="",
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
    )
    def partial_update(self, request, pk=None):
        if request.user.is_authenticated:
            serializer = WatchListRequestSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data

                watched = self.queryset.get(id=pk)
                if not watched:
                    raise APIException(
                        "watch list entry not found", status.HTTP_400_BAD_REQUEST
                    )

                curr_profile = Profile.objects.get(user=request.user)
                if watched.profile != curr_profile:
                    raise PermissionDenied()

                watched.watched = data.get("watched")
                watched.save(update_fields=["watched"])

                serializer = WatchedRetrieveSerializer(watched)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        else:
            return NotAuthenticated()
