from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Profile

User = get_user_model()

class UsersRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]

class UsersPostSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProfilePostSerializer(serializers.ModelSerializer):
    user = UsersPostSerializer()

    class Meta:
        model = Profile
        fields = ["user", "first_name", "last_name"]

class ProfileRetrieveSerializer(serializers.ModelSerializer):
    user = UsersRetrieveSerializer()

    class Meta:
        model = Profile
        fields = ["user", "first_name", "last_name"]

class UserPkSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]

class ProfilePkSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ["user"]
