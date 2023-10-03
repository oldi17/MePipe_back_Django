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
from creator.models import Creator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files import File


from creator.renderers import CreatorJSONRenderer
from creator.serializers import CreatorModelSerializer
import MePipe.settings as settings
from video.models import Video


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def registerCreator(req):
    creator = req.data.dict()
    if not creator.get('channel_background', None):
        creator['channel_background'] = File(open(os.path.join(settings.STATIC_ROOT, 'cbg.png'), 'rb'))
    creator['user_id'] = req.user.id
    serializer = CreatorModelSerializer(data=creator)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([CreatorJSONRenderer])
def getCreatorByName(req, name):
    try:
      creator = Creator.objects.get(name = name)
    except ObjectDoesNotExist as err:
        raise NotFound('No such creator')
    serializer = CreatorModelSerializer(creator, context={'req': req})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([CreatorJSONRenderer])
def getCreatorById(req, id):
    try:
      creator = Creator.objects.get(id = id)
    except ObjectDoesNotExist as err:
        raise NotFound('No such creator')
    serializer = CreatorModelSerializer(creator, context={'req': req})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
def getMe(req):
    try:
      creator = Creator.objects.get(user_id = req.user.id)
    except ObjectDoesNotExist as err:
        raise NotFound('No such creator')
    serializer = CreatorModelSerializer(creator)
    res = serializer.data
    res['views'] = getViewsNumber(creator.name)
    return Response(res, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def modifyCreator(req):
    try:
        creator = Creator.objects.get(user_id = req.user.id)
    except:
        raise NotFound('No such creator')
    serializer_data = req.data.dict()
    serializer = CreatorModelSerializer(
        creator, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeCreator(req):
    try:
        creator = Creator.objects.get(user_id = req.user.id)
    except:
        raise NotFound('No such creator')
    creator.delete()
    return Response('removed', status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
def subscribeToCreator(req, name):
    return manageSubscription(req, name, 'subscribe')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CreatorJSONRenderer])
def unsubscribeToCreator(req, name):
    return manageSubscription(req, name, 'unsubscribe')

def manageSubscription(req, name, method):
    try:
      creator = Creator.objects.get(name = name)
    except ObjectDoesNotExist as err:
        raise NotFound('No such creator')
    getattr(creator, method)(req.user)
    serializer = CreatorModelSerializer(creator, context={'req': req})
    return Response(serializer.data, status=status.HTTP_200_OK)

def getViewsNumber(creator_name):
    views = 0
    for v in Video.objects.filter(creator_name = creator_name):
        views += v.views
    return views