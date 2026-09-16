from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class RegistrationSerializer(RegisterSerializer):
    def validate_username(self, value):
        if get_user_model().objects.filter(username__iexact=value.strip()).exists():
            raise serializers.ValidationError('이미 가입된 username입니다.')
        return super().validate_username(value.strip())

    def validate_email(self, value):
        value = value.strip().lower()
        if not value:
            raise serializers.ValidationError('이메일을 입력해주세요.')
        if get_user_model().objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('이미 가입된 이메일입니다.')
        return super().validate_email(value)
