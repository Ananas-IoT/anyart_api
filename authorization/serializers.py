from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db import transaction, IntegrityError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from jwt.compat import text_type
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authorization.models import (
    UserProfile,
    BasicUserProfile,
    ArtistUserProfile,
    GovernmentUserProfile)
from authorization.tokens import account_activation_token


class UserModelSerializer(serializers.ModelSerializer):
    """Parent class which includes common logic of all User model Serializers"""

    rights = serializers.CharField(required=False)

    class Meta:
        model = get_user_model()
        fields = '__all__'

    """Property to determine which nested serializer to use for UserProfile"""
    def get_user_profile_class(self, rights=None, *args, **kwargs):
        if not rights:
            rights = self.validated_data['rights']
        return {
            'basic': BasicUserProfile,
            'artist': ArtistUserProfile,
            'gov': GovernmentUserProfile
        }[rights]
    user_profile_class = property(get_user_profile_class)

    def get_user_profile(self, *args, **kwargs):
        user_profile = self.get_user_profile_class(*args, **kwargs)
        return user_profile.objects.create(*args, **kwargs)

    def get_user_profile_serializer(self, rights=None, *args, **kwargs):
        if not rights:
            rights = self.data['rights']
        return {
            'basic': BasicUserProfileSerializer,
            'artist': ArtistUserProfileSerializer,
            'gov': GovUserProfileSerializer
        }[rights]
    user_profile_serializer = property(get_user_profile_serializer)


class RegisterUserSerializer(UserModelSerializer):
    """Serializer for creating user objects."""
    rights = serializers.CharField(required=True)

    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email',
                  'access', 'refresh', 'rights')
        extra_kwargs = {'password': {'write_only': True}}

    def get_access(self, user):
        tokens = RefreshToken.for_user(user)

        # Add custom claims to payload
        tokens['rights'] = user.rights

        access = text_type(tokens.access_token)
        return access

    def get_refresh(self, user):
        tokens = RefreshToken.for_user(user)

        # Add custom claims to payload
        tokens['rights'] = user.rights

        refresh = text_type(tokens)
        return refresh

    def create(self, validated_data):
        user_class = get_user_model()
        try:
            user = user_class.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                rights=validated_data['rights']
            )
        except Exception:
            raise serializers.ValidationError

        user.set_password(validated_data['password'])
        try:
            with transaction.atomic():
                user.save()
                user_profile = self.get_user_profile(
                    owner=user,
                )

                # request = self.context.get('view').request
                # send_verification_email(user, request)

                user_profile.save()
        except IntegrityError:
            return exceptions.ValidationError

        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class BasicUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicUserProfile
        fields = '__all__'


class ArtistUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistUserProfile
        fields = '__all__'


class GovUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernmentUserProfile
        fields = '__all__'


class MyTokenObtainPairSerializer(UserModelSerializer, TokenObtainPairSerializer):
    """Serializer for retrieving a fresh pair of tokens to already registered user"""
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['rights'] = user.rights

        return token


class ReadOnlyUserSerializer(UserModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyUserSerializer, self).__init__(*args, **kwargs)

        self.fields['user_profile'] = self.user_profile_serializer(many=False, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'rights')
        extra_kwargs = {'password': {'write_only': True}}


def send_verification_email(user, request):
    """Composes and sends email with verification token to selected email"""
    from django.contrib.sites.shortcuts import get_current_site

    user.is_active = False
    user.save()
    mail_subject = 'Activate your blog account.'
    message = render_to_string('activate_email.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()