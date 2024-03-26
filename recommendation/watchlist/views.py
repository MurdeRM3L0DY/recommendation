from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import APIException, NotAuthenticated, PermissionDenied
from rest_framework.request import Request

# from rest_framework.mixins import UpdateModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from recommendation.watchlist.models import WatchList
from recommendation.watchlist.serializers import (
    WatchListCreateSerializer,
    WatchListRequestSerializer,
    WatchListSerializer,
    WatchedRetrieveSerializer,
)

User = get_user_model()


class WatchListViewSet(GenericViewSet):
    queryset = WatchList.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return WatchListSerializer

        if self.action == "create":
            return WatchListCreateSerializer

        if self.action == "partial_update":
            return WatchListRequestSerializer

        return super().get_serializer_class()

    def list(self, request: Request):
        if request.user.is_authenticated:
            serializer = WatchListSerializer(
                self.queryset.filter(user=request.user), many=True
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
                if not movie:
                    raise APIException("invalid movie_id", status.HTTP_400_BAD_REQUEST)

                new_watched, created = self.queryset.get_or_create(
                    user=request.user,
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
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated()

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
    def partial_update(self, request, pk=None):
        if request.user.is_authenticated:
            serializer = WatchListRequestSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data

                watched = self.queryset.filter(id=pk).first()
                if not watched:
                    raise APIException(
                        "watch list entry not found", status.HTTP_400_BAD_REQUEST
                    )

                if watched.user != request.user:
                    raise PermissionDenied()

                watched.watched = data.get("watched")
                watched.save(update_fields=["watched"])

                serializer = WatchedRetrieveSerializer(watched)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        else:
            return NotAuthenticated()
