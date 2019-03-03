from rest_framework.views import APIView
from rest_framework.response import Response



class HelloView(APIView):
    # permission_classes = (IsAuthenticated, IsArtist)

    def get(self, request, *args, **kwargs):
        content = {
            'message': 'Hello, World!',
        }
        return Response('Hello World')

    def post(self, request):
        return Response(request.data)