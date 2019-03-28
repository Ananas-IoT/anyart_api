from rest_framework import status
from rest_framework.response import Response
import copy

from rest_framework import viewsets

from authorization.permissions import retrieve_payload
from workload.serializers import (WallPhotoWrapperSerializer, SketchSerializer,
                                  WallPhotoSerializer, WorkloadSerializer,
                                  SketchImageSerializer, LocationSerializer, ReadOnlyWorkloadSerializer,
                                  LimitationSerializer)
from .models import WallPhotoWrapper, Sketch, WallPhoto, Workload, SketchImage, Location


class WorkloadViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Workload.objects.all()
    serializer_class = WorkloadSerializer

    def create(self, request, *args, **kwargs):
        ser_data = copy.deepcopy(request.data)
        # User Id retrieval
        try:
            user_id = retrieve_payload(request)['user_id']
        except KeyError:
            return Response('Either token is invalid or not present', status=status.HTTP_401_UNAUTHORIZED)
        ser_data['user_id'] = user_id

        # Serializer
        serializer = self.get_serializer(data=ser_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        # Serializer
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadOnlyWorkloadSerializer
        return WorkloadSerializer


class WallPhotoWrapperViewSet(viewsets.ModelViewSet):
    queryset = WallPhotoWrapper.objects.all()
    serializer_class = WallPhotoWrapperSerializer

    def create(self, request, *args, **kwargs):
        ser_data = copy.deepcopy(request.data)
        # User Id retrieval
        try:
            user_id = retrieve_payload(request)['user_id']
        except KeyError:
            return Response('Either token is invalid or not present', status=status.HTTP_401_UNAUTHORIZED)
        ser_data['user_id'] = user_id

        # Lookup fields & foreign keys
        # if data contains no workload_id, fetch it from url
        try:
            if not ser_data.get('workload_pk'):
                ser_data['workload_id'] = kwargs['workload_pk']
        except KeyError:
            return Response('Unable to retrieve workload_id', status=status.HTTP_400_BAD_REQUEST)

        # Serializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        # Serializer
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return WallPhotoWrapper.objects.filter(workload=self.kwargs.pop('workload_pk', None)) or \
               WallPhotoWrapper.objects.all()


class SketchViewSet(viewsets.ModelViewSet):
    queryset = Sketch.objects.all()
    serializer_class = SketchSerializer

    def create(self, request, *args, **kwargs):
        ser_data = copy.deepcopy(request.data)
        # User Id retrieval
        try:
            user_id = retrieve_payload(request)['user_id']
        except KeyError:
            return Response('Either token is invalid or not present', status=status.HTTP_401_UNAUTHORIZED)
        ser_data['user_id'] = user_id

        # Lookup fields & foreign keys
        # if data contains no workload_id, fetch it from url
        try:
            if not ser_data.get('workload_id'):
                ser_data['workload_id'] = kwargs['workload_pk']
        except KeyError:
            return Response('Unable to retrieve workload_id', status=status.HTTP_400_BAD_REQUEST)

        # Serializer
        serializer = self.get_serializer(data=ser_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop('partial', False)

        # Serializer
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.kwargs.get('workload_pk'):
            return Sketch.objects.filter(workload=self.kwargs.get('workload_pk', None))
        return Sketch.objects.all()


class WallPhotoViewSet(viewsets.ModelViewSet):
    queryset = WallPhoto.objects.all()
    serializer_class = WallPhotoSerializer

    def create(self, request, wall_photo_wrapper_pk=None, *args, **kwargs):
        ser_data = copy.deepcopy(request.data)
        # User Id retrieval
        try:
            user_id = retrieve_payload(request)['user_id']
        except KeyError:
            return Response('Either token is invalid or not present', status=status.HTTP_401_UNAUTHORIZED)
        ser_data['user_id'] = user_id

        # Lookup fields & foreign keys
        # if data contains no wall_photo_wrapper_pk, fetch it from url
        try:
            if not ser_data.get('wall_photo_wrapper_id'):
                ser_data['wrapper'] = wall_photo_wrapper_pk
        except KeyError:
            return Response('Unable to retrieve wall_photo_wrapper_pk_id', status=status.HTTP_400_BAD_REQUEST)

        # Serializer
        serializer = self.get_serializer(data=ser_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return WallPhoto.objects.filter(wrapper=self.kwargs.pop('wall_photo_wrapper_pk', None)) \
               or WallPhoto.objects.all()


class SketchImageViewSet(viewsets.ModelViewSet):
    queryset = SketchImage.objects.all()
    serializer_class = SketchImageSerializer

    def create(self, request, sketch_pk=None, *args, **kwargs):
        ser_data = copy.deepcopy(request.data)

        # Lookup fields & foreign keys
        # if data contains no sketch_pk, fetch it from url
        try:
            if not ser_data.get('sketch_pk'):
                ser_data['sketch_pk'] = sketch_pk
        except KeyError:
            return Response('Unable to retrieve sketch_pk', status=status.HTTP_400_BAD_REQUEST)

        # Serializer
        serializer = self.get_serializer(data=ser_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return SketchImage.objects.filter(sketch_id=self.kwargs['sketch_pk'])


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(photo_wrapper=self.kwargs.pop('workload_pk', None)) \
               or Location.objects.all()


class LimitationViewSet(viewsets.ModelViewSet):
    serializer_class = LimitationSerializer