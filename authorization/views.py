from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from authorization.serializers import RegisterUserSerializer, MyTokenObtainPairSerializer


class UserListView(generics.ListCreateAPIView):
    """Handles creating and listing Users."""
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        rights = request.data.pop('rights')
        serializer = RegisterUserSerializer(data=request.data, context={'rights': rights})
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer