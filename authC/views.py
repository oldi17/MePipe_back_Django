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


from authC.tokens import create_jwt_pair_for_user
from .renderers import UserJSONRenderer
from .serializers import (
    RegistrationSerializer, UserSerializer, LoginSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
@renderer_classes([UserJSONRenderer])
def registerUser(req):
    user = req.data.get('user', {})
    serializer = RegistrationSerializer(data=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def loginUser(req):
    user = req.data.get('user', {})
    serializer = LoginSerializer(data=user)
    serializer.is_valid(raise_exception=True)
    tokens = create_jwt_pair_for_user(serializer.validated_data)
    return Response(tokens, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutUser(req):
    refresh_token = req.data.get('refresh')
    try:
      token = RefreshToken(token=refresh_token)
      token.blacklist()
    except TokenError as e:
        return Response({"status": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"status": "OK, goodbye"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserJSONRenderer])
def getUser(req):
    serializer = UserSerializer(req.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['UPDATE'])
@permission_classes([IsAuthenticated])
@renderer_classes([UserJSONRenderer])
def updateUser(req):
    serializer_data = req.data.get('user', {})
    serializer = UserSerializer(
        req.user, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)