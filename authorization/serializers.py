from django.contrib.auth.models import User
from jwt.compat import text_type
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authorization.models import UserProfile


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for creating user objects."""

    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'access', 'refresh')
        extra_kwargs = {'password': {'write_only': True}}

    def get_access(self, user):
        tokens = RefreshToken.for_user(user)

        # Add custom claims to payload
        tokens['rights'] = UserProfile.objects.filter(user=user).get().rights

        access = text_type(tokens.access_token)
        return access

    def get_refresh(self, user):
        tokens = RefreshToken.for_user(user)

        # Add custom claims to payload
        tokens['rights'] = UserProfile.objects.filter(user=user).get().rights

        refresh = text_type(tokens)
        return refresh

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        user_profile = UserProfile(
            user=user,
            rights=self.context['rights']
        )
        user_profile.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['rights'] = UserProfile.objects.filter(user=user).get().rights

        return token