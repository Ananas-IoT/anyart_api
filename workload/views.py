from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from anyart_api.parsers import NestedMultipartParser
from workload.serializers import DocumentSerializer, UserWallUploadSerializer
from .models import Document, Workload


class WallPhotoView(APIView):
    parser_classes = (NestedMultipartParser, )

    def post(self, request):
        serializer = UserWallUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class DocumentCreateView(CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DocumentRetrieveView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
