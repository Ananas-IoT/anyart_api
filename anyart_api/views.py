from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authorization.permissions import IsArtist


class HelloView(APIView):
    permission_classes = (IsAuthenticated, IsArtist)

    def get(self, request):
        content = {
            'message': 'Hello, World!',
        }
        return Response(content)