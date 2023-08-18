from django.contrib.auth import get_user_model
from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    def validate_email(self, value):
        if not value.endswith("@ed.tus.ac.jp"):
            raise serializers.ValidationError("メールアドレスの形式は「@ed.tus.ac.jp」です")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")
