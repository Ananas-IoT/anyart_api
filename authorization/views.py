from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view
import copy
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authorization.serializers import RegisterUserSerializer, MyTokenObtainPairSerializer, ReadOnlyUserSerializer
from authorization.tokens import account_activation_token, password_activation_token
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
import pdb

class UserCreateView(generics.CreateAPIView):
    """Handles creating Users."""
    user_class = get_user_model()
    queryset = user_class.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(http_method_names=['GET'])
def profile(request):
    serializer = ReadOnlyUserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=['GET'])
def verify_email(request, uidb64, token):
    user_class = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user_class.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user_class.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


"""
-------------------------'Forgot Password' Section ---------------------------
"""

@api_view(http_method_names=['POST'])
def forgot_password(request, *args, **kwargs):
    try: 
        email = request.data.get('email')   
    except KeyError:
        return Response("Not all fields were sent. Required fields are: email",
                        status=status.HTTP_400_BAD_REQUEST)
        
    try:
        user_model = get_user_model()
        user = user_model.objects.get(email=email)
    except user_model.DoesNotExist:
        return Response("User doesn't exist", 400)
    send_password_reset(user)
    return Response('Email sent', status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
def verify_reset_code(request, *args, **kwargs):
    try: 
        email = request.data['email']
        reset_code = request.data['reset_code']
    except KeyError:
        return Response("Not all fields were sent. Required fields are: email, reset_code",
                        status=status.HTTP_400_BAD_REQUEST)
    user = get_user_model().objects.get(email=email)
    allowed_change = account_activation_token.check_token(user, reset_code)
    if allowed_change:
        token = password_activation_token.make_token(user)
        # pdb.set_trace()
        return Response({'password_token': token}, status=status.HTTP_200_OK)
    return Response("Not allowed to change password", status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
def change_password(request, *args, **kwargs):
    try:
        email = request.data['email']
        password_token = request.data['password_token']
        new_password = request.data['new_password']
    except KeyError:
        return Response("Not all fields were sent. Required fields are: password_token, new_password, email",
                        status=status.HTTP_400_BAD_REQUEST)
    user_model = get_user_model()
    user = user_model.objects.get(email=email)
    allowed_change = password_activation_token.check_token(user, password_token)
    if allowed_change:
        user.set_password(new_password)
        user.save()
        return Response("Password changed", status=status.HTTP_200_OK)
    return Response("Not allowed to change password", status=status.HTTP_400_BAD_REQUEST)


def send_password_reset(user):
    # todo make token expire after use
    mail_subject = 'Password reset request'
    reset_code = account_activation_token.make_token(user)
    message = render_to_string('forgot_password.html', {
        'user': user,
        'reset_code': reset_code
    })

    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )

    email.send()
