from rest_framework import viewsets, status
from rest_framework.response import Response

from anyart_api.parsers import NestedMultipartParser
from authorization.permissions import retrieve_payload
from workload.serializers import WallPhotoWrapperSerializer, SketchSerializer, WallPhotoSerializer
from .models import WallPhotoWrapper, Sketch, WallPhoto


class WallPhotoWrapperViewSet(viewsets.ModelViewSet):
    parser_classes = (NestedMultipartParser, )
    queryset = WallPhotoWrapper.objects.all()
    serializer_class = WallPhotoWrapperSerializer

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


class SketchViewSet(viewsets.ModelViewSet):
    parser_classes = (NestedMultipartParser, )
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


class WallPhotoViewSet(viewsets.ModelViewSet):
    parser_classes = (NestedMultipartParser, )
    queryset = WallPhoto.objects.all()
    serializer_class = WallPhotoSerializer
