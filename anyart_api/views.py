from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import re
import base64 as b
import ast

from authorization.permissions import IsArtist


class HelloView(APIView):
    permission_classes = (IsAuthenticated, IsArtist)

    def get(self, request):
        token_str = request.META['HTTP_AUTHORIZATION']
        regex = re.compile('\..*\.')
        claims = regex.findall(token_str)[0]
        claims = claims[1:-1]
        missing_data = len(claims) % 4
        claims = str(b.b64decode(claims + '=' * missing_data), 'utf-8')
        claims = ast.literal_eval(claims)
        content = {
            'message': 'Hello, World!',
            'token': request.META.get('HTTP_AUTHORIZATION'),
            'claims': claims
        }

        return Response(content)