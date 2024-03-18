from django.contrib.auth import authenticate, get_user_model, login, logout
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from recommendation.users.serializers import UsersPostSerializer, UsersRetrieveSerializer

User = get_user_model()

class AuthViewSet(GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "login":
            return UsersPostSerializer

        return Serializer

    @action(detail=False, methods=['POST'], url_path='login')
    @extend_schema(
        request=UsersPostSerializer,
        # override default docstring extraction
        description='',
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
    )
    def login(self, request):
        serializer = UsersPostSerializer(data=request.data)

        print("ffs goddamnit: ", request.headers)

        if serializer.is_valid():
            data = serializer.validated_data

            email = data.get('email')
            password = data.get('password')

            user = authenticate(request, email=email, password=password)

            if not user:
                raise AuthenticationFailed()

            login(request, user)

            serializer = UsersRetrieveSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='logout')
    def logout(self, request):
        logout(request)

        return Response(True, status.HTTP_200_OK)
