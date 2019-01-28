from rest_framework import viewsets, status
from rest_framework.response import Response

from anyart_api.parsers import NestedMultipartParser
from authorization.permissions import retrieve_payload
from workload.serializers import WallPhotoWrapperSerializer
from .models import WallPhotoWrapper


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
