from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from anyart_api.parsers import NestedMultipartParser
from authorization.permissions import IsArtist


class HelloView(APIView):
    # permission_classes = (IsAuthenticated, IsArtist)
    parser_classes = (NestedMultipartParser, )

    def get(self, request):
        content = {
            'message': 'Hello, World!',
        }
        return Response(content)

    def post(self, request):
        return Response(request.data)