# FIXME: Use a Serializer wherever possible

from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException, NotAuthenticated

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from recommendation.users.serializers import (
    UsersPkSerializer,
    UsersPostSerializer,
    UsersRetrieveSerializer,
)

User = get_user_model()


class UsersViewSet(GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UsersPostSerializer

        if self.action == "add_friend":
            return UsersPkSerializer

        return super().get_serializer_class()

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
    def create(self, request: Request, *args, **kwargs):
        serializer = UsersPostSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            first_name = data.get("first_name")
            last_name = data.get("last_name")
            email = data.get("email")
            password = data.get("password")

            if self.queryset.filter(email=email).exists():
                raise APIException("user already exists", status.HTTP_409_CONFLICT)

            new_user = self.queryset.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            new_user.save()

            serializer = UsersRetrieveSerializer(new_user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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
    def list(self, request: Request):
        serializer = UsersRetrieveSerializer(self.queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="add-friend")
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
    def add_friend(self, request: Request):
        if request.user.is_authenticated:
            serializer = UsersPkSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data

                friend = data.get("user")
                if request.user == friend:
                    raise APIException("can't add self to friend's list")

                if request.user.friends.filter(id=friend.id).exists():
                    raise APIException("user is already in friendlist")

                request.user.friends.add(friend)

                serializer = UsersRetrieveSerializer(friend)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated()
