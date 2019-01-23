from rest_framework.generics import CreateAPIView, ListAPIView

from workload.serializers import DocumentSerializer
from .models import Document


class DocumentCreateView(CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class DocumentRetrieveView(ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
