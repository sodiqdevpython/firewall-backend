from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=128)
    password = serializers.CharField(max_length=68, write_only=True)
    access_token = serializers.CharField(max_length=256, read_only=True)
    refresh_token = serializers.CharField(max_length=256, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "access_token", "refresh_token"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")

        user = authenticate(request=request, email=email, password=password)

        user_tokens = user.tokens()

        return {
            "email": user.email,
            "access_token": str(user_tokens.get("access")),
            "refresh_token": str(user_tokens.get("refresh"))
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_verified", "is_active", "date_joined", "last_login"]
        read_only_fields = ["id", "date_joined", "last_login"]
