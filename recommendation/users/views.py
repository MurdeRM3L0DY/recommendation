# FIXME: Use a Serializer wherever possible

from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException, NotAuthenticated

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from recommendation.users.models import Profile
from recommendation.users.serializers import ProfilePkSerializer, ProfilePostSerializer, ProfileRetrieveSerializer

User = get_user_model()

class UsersViewSet(GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ProfilePostSerializer

        if self.action == "add_friend":
            return ProfilePkSerializer

        return super().get_serializer_class()

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
    def create(self, request: Request, *args, **kwargs):
        serializer = ProfilePostSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            user = data.get('user')
            first_name = data.get('first_name')
            last_name = data.get('first_name')

            if self.queryset.filter(email=user.get('email')).exists():
                raise APIException("user already exists", status.HTTP_409_CONFLICT)

            new_profile = Profile.objects.create(
                first_name=first_name,
                last_name=last_name,
                user = User.objects.create_user(**user)
            )
            new_profile.save()

            serializer = ProfileRetrieveSerializer(new_profile)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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
    def list(self, request: Request):
        serializer = ProfileRetrieveSerializer(Profile.objects.all(), many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path="add-friend")
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
    def add_friend(self, request: Request):
        if request.user.is_authenticated:
            serializer = ProfilePkSerializer(data=request.data)

            if serializer.is_valid():
                data = serializer.validated_data

                curr_profile = Profile.objects.get(user=request.user)
                friend_profile = Profile.objects.get(user=data.get("user"))

                if curr_profile == friend_profile:
                    raise APIException("can't add self to friend's list")

                if curr_profile.friends.filter(user=data.get("user")).exists():
                    raise APIException("user is already in friendlist")

                curr_profile.friends.add(friend_profile)

                serializer = ProfileRetrieveSerializer(friend_profile)
                return Response(serializer.data, status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        else:
            raise NotAuthenticated()
