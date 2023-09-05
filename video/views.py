from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    parser_classes
    )
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from creator.models import Creator
from video.utils import generateURL
from .models import Video
from .renderers import VideoJSONRenderer
from .serializers import VideoModelSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([VideoJSONRenderer])
def getVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    serializer = VideoModelSerializer(video)
    video.addView()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def addVideo(req):
    try:
        creator = Creator.objects.get(user_id = req.user.id)
    except:
        raise PermissionDenied('You are not a creator yet')
  
    video = req.data
    video['creator_id'] = creator.id
    video['url'] = generateURL()
    
    serializer = VideoModelSerializer(data=video)
    serializer.is_valid(raise_exception=True)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def modifyVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    
    try:
        creator = Creator.objects.get(user_id = req.user.id)
    except:
        raise PermissionDenied('You are not a creator yet')
    
    if video.creator_id != creator:
        raise PermissionDenied('It\'s not your video')
    

    serializer_data = req.data

    serializer = VideoModelSerializer(
        video, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
def likeVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    video.like(req.user)
    serializer = VideoModelSerializer(video)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
def dislikeVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    video.dislike(req.user)
    serializer = VideoModelSerializer(video)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
def unlikeVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    video.unlike(req.user)
    serializer = VideoModelSerializer(video)
    return Response(serializer.data, status=status.HTTP_200_OK)