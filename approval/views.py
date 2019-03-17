from rest_framework import viewsets, status
import copy

from rest_framework.response import Response

from approval.models import SketchVote
from approval.serializers import SketchVoteSerializer
from authorization.permissions import retrieve_payload


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

    def get_queryset(self):
        return SketchVote.objects.filter(sketch=self.kwargs.pop('sketch_pk', None)) or \
               SketchVote.objects.all()