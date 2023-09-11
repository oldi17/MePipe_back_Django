from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    parser_classes,
    )
from creator.models import Creator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser

from creator.renderers import CreatorJSONRenderer
from creator.serializers import CreatorModelSerializer
from authC.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def registerCreator(req):
    creator = req.data
    creator['user_id'] = req.user.id
    serializer = CreatorModelSerializer(data=creator)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([CreatorJSONRenderer])
def getCreator(req, name):
    try:
      creator = Creator.objects.get(name = name)
    except ObjectDoesNotExist as err:
        raise NotFound('No such creator')
    serializer = CreatorModelSerializer(creator)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def modifyCreator(req):
    try:
        creator = Creator.objects.get(user_id = req.user.id)
    except:
        raise NotFound('No such creator')
    serializer_data = req.data
    serializer = CreatorModelSerializer(
        creator, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)