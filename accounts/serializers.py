from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework import serializers

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    type = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "type",
            "password",
            "full_name"
        )

class CustomUserSerializer(UserSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    type = serializers.CharField(write_only=True, default='H')
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            "type_display",
            "type",
            "full_name"
        )
        read_only_fields = (settings.LOGIN_FIELD,)
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)