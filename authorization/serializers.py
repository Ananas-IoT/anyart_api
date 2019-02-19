from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from jwt.compat import text_type
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from authorization.models import UserProfile
from authorization.tokens import account_activation_token


class RegisterUserSerializer(serializers.ModelSerializer):
    """Serializer for creating user objects."""
    rights = serializers.CharField(required=True, write_only=True)

    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email',
                  'access', 'refresh', 'rights')
        extra_kwargs = {'password': {'write_only': True}}

    def get_access(self, user):
        tokens = RefreshToken.for_user(user)

        # Add custom claims to payload
        tokens['rights'] = UserProfile.objects.filter(owner=user).get().rights

        access = text_type(tokens.access_token)
        return access

    def get_refresh(self, user):
        tokens = RefreshToken.for_user(user)

        # Add custom claims to payload
        tokens['rights'] = UserProfile.objects.filter(owner=user).get().rights

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
            owner=user,
            rights=validated_data['rights']
        )

        request = self.context.get('view').request
        send_verification_email(user, request)
        user_profile.save()

        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['rights'] = UserProfile.objects.filter(owner=user).get().rights

        return token


class ReadOnlyUserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'user_profile')
        extra_kwargs = {'password': {'write_only': True}}


def send_verification_email(user, request):
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
