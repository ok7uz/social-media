from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken, Token

from apps.posts.models import Tag

from .models import Interest, User, Follow


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'bio', 'birth_date', 'profile_picture',
            'cover_image', 'posts_count', 'followers_count', 'following_count'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PUT':
            for field in self.fields.values():
                field.required = False


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_picture', 'cover_image')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = PasswordField(write_only=True)

    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise AuthenticationFailed()

        data = {}
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        update_last_login(None, user)
        return data

    @staticmethod
    def get_token(user) -> Token:
        return RefreshToken.for_user(user)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'first_name', 'last_name', 'bio', 'birth_date', 'profile_picture'
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'] if 'last_name' in validated_data else None,
            bio=validated_data['bio'] if 'bio' in validated_data else None,
            birth_date=validated_data['birth_date'] if 'birth_date' in validated_data else None,
            profile_picture=validated_data['profile_picture'] if 'profile_picture' in validated_data else None,
            cover_image=validated_data['cover_image'] if 'cover_image' in validated_data else None
        )
        user.set_password(validated_data.pop('password'))
        user.save()
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'password fields did not match'}
            )
        return attrs


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

    def create(self, validated_data):
        follow, _ = Follow.objects.get_or_create(**validated_data)
        return follow

    def validate(self, attrs):
        if attrs['follower'] == attrs['following']:
            raise serializers.ValidationError('You cannot follow yourself')
        return attrs


class InterestSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        fields = ('tags',)

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags')
        Interest.objects.filter(user=user).delete()
        for tag in tags:
            tag_instance, _ = Tag.objects.get_or_create(name=tag)
            Interest.objects.get_or_create(user=user, tag=tag_instance)
        return {'tags': tags}

    