from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(request=self.context['request'], username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                {
                    'non_field_errors': _('Unable to log in with provided credentials.')
                }
            )
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    'non_field_errors': _('User account is disabled.')
                }
            )
        attrs['user'] = user
        return attrs


class UserRegisterSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True, source='auth_token.key')

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password2', 'token')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise ValidationError({'message': 'password and password2 must match'})

        if User.objects.filter(email=instance['email']).exists():
            raise ValidationError({'message': 'Email already taken'})

        return instance

    def create(self, validated_data):
        password = validated_data.pop('password')
        _ = validated_data.pop('password2')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user


class UserLoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class EmptyBodySerializer(serializers.Serializer):
    pass
