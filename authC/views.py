from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    )
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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