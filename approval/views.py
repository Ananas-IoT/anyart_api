from django.contrib.auth.decorators import permission_required
from rest_framework import viewsets, status
import copy

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from approval.models import SketchVote, SketchDecision, WallPhotoWrapperDecision
from approval.serializers import SketchVoteSerializer, SketchDecisionSerializer, WallPhotoWrapperDecisionSerializer
from authorization.permissions import retrieve_payload, IsOwner


class SketchVoteViewSet(viewsets.ModelViewSet):
    serializer_class = SketchVoteSerializer
    queryset = SketchVote.objects.all()

    def create(self, request, sketch_pk=None, *args, **kwargs):
        # retrieve user pk
        try:
            user_id = retrieve_payload(request)['user_id']
        except KeyError:
            return Response('Either token is invalid or not present', status=status.HTTP_401_UNAUTHORIZED)
        ser_data = copy.deepcopy(request.data)
        ser_data['owner'] = user_id

        # Lookup fields & foreign keys
        # if data contains no sketch, fetch it from url
        try:
            if not ser_data.get('sketch'):
                ser_data['sketch'] = sketch_pk
        except KeyError:
            return Response('Unable to retrieve sketch_id', status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=ser_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, sketch_pk=None, *args, **kwargs):
        instance = self.get_object()
        ser_data = copy.deepcopy(request.data)
        partial = kwargs.pop('partial', False)
        # Lookup fields & foreign keys
        # if data contains no sketch, fetch it from url
        try:
            if not ser_data.get('sketch'):
                ser_data['sketch'] = sketch_pk
        except KeyError:
            return Response('Unable to retrieve sketch_id', status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=ser_data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return SketchVote.objects.filter(sketch=self.kwargs.pop('sketch_pk', None)) or \
               SketchVote.objects.all()


class SketchDecisionViewSet(viewsets.ModelViewSet):
    http_method_names = ['put', 'patch', 'get']
    queryset = SketchDecision.objects.all()
    serializer_class = SketchDecisionSerializer

    def update(self, request, *args, **kwargs):
        # retrieve user pk
        try:
            user = request.user
        except KeyError:
            return Response('Either token is invalid or not present', status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        ser_data = copy.deepcopy(request.data)
        ser_data['owner_pk'] = user.id

        serializer = self.get_serializer(instance, data=ser_data, partial=kwargs.get('partial'))
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        groups = []
        for group in self.request.user.groups.all():
            groups.append(group)

        if self.kwargs.get('sketch_pk', None) is not None:
            return SketchDecision.objects \
                .filter(sketch_id=self.kwargs.get('sketch_pk', None), group_role__in=groups)
        else:
            return SketchDecision.objects.filter(group_role__in=groups)


class WallPhotoWrapperDecisionViewSet(viewsets.ModelViewSet):
    http_method_names = ['put', 'patch', 'get']
    queryset = WallPhotoWrapperDecision.objects.all()
    serializer_class = WallPhotoWrapperDecisionSerializer

    def update(self, request, *args, **kwargs):
        # retrieve user pk
        try:
            user = request.user
        except KeyError:
            return Response('Either token is invalid or not present', status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        ser_data = copy.deepcopy(request.data)
        ser_data['owner_pk'] = user.id

        serializer = self.get_serializer(instance, data=ser_data, partial=kwargs.get('partial'))
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'serializer': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        groups = []
        for group in self.request.user.groups.all():
            groups.append(group)

        if self.kwargs.get('wall_photo_wrapper_pk', None) is not None:
            return WallPhotoWrapperDecision.objects \
                .filter(wall_photo_wrapper_id=self.kwargs.get('wall_photo_wrapper_pk', None), group_role__in=groups)
        else:
            return WallPhotoWrapperDecision.objects.filter(group_role__in=groups)
