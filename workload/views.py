from rest_framework import viewsets, status
from rest_framework.response import Response

from authorization.permissions import retrieve_payload
from workload.serializers import (WallPhotoWrapperSerializer, SketchSerializer,
                                  WallPhotoSerializer, WorkloadSerializer,
                                  SketchImageSerializer, LocationSerializer, ReadOnlyWorkloadSerializer)
from .models import WallPhotoWrapper, Sketch, WallPhoto, Workload, SketchImage, Location


class WallPhotoWrapperViewSet(viewsets.ModelViewSet):
    queryset = WallPhotoWrapper.objects.all()
    serializer_class = WallPhotoWrapperSerializer

    def create(self, request, *args, **kwargs):
        user_id = retrieve_payload(request)['user_id']
        request.data['user_id'] = user_id
        request.data['workload_id'] = kwargs['workload_pk']
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user_id = retrieve_payload(request)['user_id']
        request.data['user_id'] = user_id
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return WallPhotoWrapper.objects.filter(workload=self.kwargs.pop('workload_pk', None)) or WallPhotoWrapper.objects.all()


class SketchViewSet(viewsets.ModelViewSet):
    queryset = Sketch.objects.all()
    serializer_class = SketchSerializer

    def create(self, request, *args, **kwargs):
        user_id = retrieve_payload(request)['user_id']
        request.data['user_id'] = user_id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user_id = retrieve_payload(request)['user_id']
        request.data['user_id'] = user_id
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Sketch.objects.filter(workload=self.kwargs['workload_pk'])


class WallPhotoViewSet(viewsets.ModelViewSet):
    queryset = WallPhoto.objects.all()
    serializer_class = WallPhotoSerializer

    def get_queryset(self):
        return WallPhotoWrapper.objects.filter(workload=self.kwargs['wall_photo_wrapper_pk'])


class SketchImageViewSet(viewsets.ModelViewSet):
    queryset = SketchImage.objects.all()
    serializer_class = SketchImageSerializer

    def get_queryset(self):
        return SketchImage.objects.filter(workload=self.kwargs['sketch_pk'])


class WorkloadViewSet(viewsets.ModelViewSet):
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer

    def create(self, request, *args, **kwargs):
        user_id = retrieve_payload(request)['user_id']
        request.data['user_id'] = user_id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user_id = retrieve_payload(request)['user_id']
        request.data['user_id'] = user_id
        instance = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return ReadOnlyWorkloadSerializer
        return WorkloadSerializer


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(photo_wrapper=self.kwargs.pop('wall_photo_wrapper_pk', None)) or Location.objects.all()