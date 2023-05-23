from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework import serializers

User = get_user_model()


class CustomChoiceField(serializers.ChoiceField):
    def to_representation(self, value):
        if value in ('', None):
            return value
        return self.choices.get(str(value), value)



class CustomUserCreateSerializer(UserCreateSerializer):
    type = CustomChoiceField(choices=User.TYPE_CHOICES, required=True)
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
    type = CustomChoiceField(choices=User.TYPE_CHOICES)
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            "type",
            "full_name"
        )
        read_only_fields = (settings.LOGIN_FIELD,)
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)