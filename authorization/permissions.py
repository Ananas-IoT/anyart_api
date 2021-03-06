from rest_framework import permissions, serializers
import re
import ast
import base64 as b


def retrieve_payload(request):
    token_str = request.META['HTTP_AUTHORIZATION']
    regex = re.compile('\..*\.')
    try:
        payload = regex.findall(token_str)[0]
    except IndexError:
        raise serializers.ValidationError('Cannot retrieve payload')
    payload = payload[1:-1]

    missing_data = len(payload) % 4
    payload = str(b.b64decode(payload + '=' * missing_data), 'utf-8')
    payload = ast.literal_eval(payload)

    return payload


class IsArtist(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            payload = retrieve_payload(request)
            return payload['rights'] == 'artist'
        except KeyError:
            return False


class IsBasic(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            payload = retrieve_payload(request)
            return payload['rights'] == 'basic'
        except KeyError:
            return False


class IsGov(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            payload = retrieve_payload(request)
            return payload['rights'] == 'gov'
        except KeyError:
            return False


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return True

    def has_object_permission(self, request, view, obj):
        try:
            payload = retrieve_payload(request)
            return payload['user_id'] == obj.owner.id
        except KeyError:
            return False


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            payload = retrieve_payload(request)
            return payload['user_id'] == obj.id
        except KeyError:
            return False