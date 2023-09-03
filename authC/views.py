from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    )
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from authC.tokens import createJWTPairForUser
from .renderers import UserJSONRenderer
from .serializers import (
    UserModelSerializer, LoginSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
@renderer_classes([UserJSONRenderer])
def registerUser(req):
    user = req.data.get('user', {})
    user['logo'] = '/static/PfPs/'+ user['username'] +'.png'
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
    tokens = createJWTPairForUser(serializer.validated_data)
    return Response(tokens, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserJSONRenderer])
def getUser(req):
    serializer = UserModelSerializer(req.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserJSONRenderer])
def modifyUser(req):
    serializer_data = req.data.get('user', {})
    serializer = UserModelSerializer(
        req.user, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)