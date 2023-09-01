from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    )
from api.models import Creator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from api.renderers import CreatorJSONRenderer
from api.serializers import CreatorModelSerializer
from authC.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
def registerCreator(req):
    creator = req.data.get('creator', {})
    creator['user_id'] = req.user.id
    serializer = CreatorModelSerializer(data=creator)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([CreatorJSONRenderer])
def getCreator(req, username):
    try:
      user_id = User.objects.get(username = username).id
      creator = Creator.objects.get(user_id = user_id)
    except ObjectDoesNotExist as err:
        raise NotFound('No such creator')
        # return Response({'code': 'no such creator'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = CreatorModelSerializer(creator)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
def modifyCreator(req):
    creator = Creator.objects.get(user_id = req.user.id)
    serializer_data = req.data.get('creator', {})
    serializer = CreatorModelSerializer(
        creator, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)