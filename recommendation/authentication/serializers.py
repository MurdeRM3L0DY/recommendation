from rest_framework import serializers


class AuthPostSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
