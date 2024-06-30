from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken, Token

from apps.posts.models import Tag
from .models import User, Follow


class InterestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ('id', 'name')
        

class UserSerializer(serializers.ModelSerializer):
    interest_list = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'bio', 'birth_date', 'profile_picture',
            'cover_image', 'post_count', 'follower_count', 'following_count', 'interest_list', 'interests',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'PUT':
            for field in self.fields.values():
                field.required = False
                
    def update(self, instance, validated_data):
        interests = validated_data.pop('interest_list', None)
        super().update(instance, validated_data)
        if interests:
            instance.interests.clear()
            for interest in interests:
                tag, _ = Tag.objects.get_or_create(name=interest)
                instance.interests.add(tag)
        return instance


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
    # interest_list = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    # interests = InterestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2', 'first_name', 'last_name'
        )

    def create(self, validated_data):
        # interests = validated_data.pop('interest_list', [])
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            # bio=validated_data.get('bio', ''),
            # birth_date=validated_data.get('birth_date', None),
            # profile_picture=validated_data.get('profile_picture', None),
            # cover_image=validated_data.get('cover_image', None)
        )
        # for interest in interests:
        #     tag, _ = Tag.objects.get_or_create(name=interest)
        #     user.interests.add(tag)
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

    
