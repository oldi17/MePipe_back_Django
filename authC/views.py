import os
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    parser_classes,
    )
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files import File


from authC.tokens import createJWTPairForUser
from .renderers import UserJSONRenderer
from .serializers import (
    UserModelSerializer, LoginSerializer
)
import MePipe.settings as settings

@api_view(['POST'])
@permission_classes([AllowAny])
@renderer_classes([UserJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def registerUser(req):
    user = req.data
    if not user.get('logo', None):
        user = user.copy()
        user['logo'] = File(open(os.path.join(settings.STATIC_ROOT, 'anon.png'), 'rb'))
    serializer = UserModelSerializer(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(req):
    user = req.data.get('user', {})
    serializer = LoginSerializer(data=user)
    serializer.is_valid(raise_exception=True)
    tokens, user = serializer.validated_data
    data = {
        'user': UserModelSerializer(user).data,
    }
    data.update(tokens)
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserJSONRenderer])
def reqUser(req):
    if req.method == 'GET':
        return getUser(req)
    if req.method == 'PATCH':
        return modifyUser(req)

def getUser(req):
    serializer = UserModelSerializer(req.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@parser_classes([MultiPartParser, FormParser])
def modifyUser(req):
    serializer_data = req.data
    serializer = UserModelSerializer(
        req.user, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)