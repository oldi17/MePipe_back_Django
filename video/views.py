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
from .models import Video, HistoryVideo
from .renderers import HistoryVideoJSONRenderer, VideoJSONRenderer
from .serializers import VideoModelSerializer, HistoryVideoModelSerializer
from MePipe.utils import paginate

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllHistoryVideo(req):
    historyVideo = HistoryVideo.objects \
        .filter(user_id = req.user.id) \
        .order_by('-watchedAt')
    return paginate(historyVideo, req, HistoryVideoModelSerializer, 'historyVideos')

@api_view(['GET'])
@permission_classes([AllowAny])
def getCreatorVideo(req, id):
    video = Video.objects \
        .filter(creator_id = id) \
        .order_by('-id')
    return paginate(video, req, VideoModelSerializer, 'videos')

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllVideo(req):
    video = Video.objects.all().order_by('-id')
    return paginate(video, req, VideoModelSerializer, 'videos')

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([VideoJSONRenderer])
def getVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    serializer = VideoModelSerializer(video, context={'req': req})

    video.addView()
    
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([HistoryVideoJSONRenderer])
def getHistoryVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    historyVideo = {
        'user_id': req.user.id, 
        'video_url': video.url
    }
    serializer = HistoryVideoModelSerializer(data=historyVideo)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([HistoryVideoJSONRenderer])
def setHistoryVideoTime(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    serializer_data = {
        'user_id': req.user.id, 
        'video_url': video.url,
    }
    try:
        historyVideo = HistoryVideo.objects.get(**serializer_data)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video in history')
    serializer_data['time'] = req.data.get('historyVideo', {}).get('time', 0)
    serializer = HistoryVideoModelSerializer(historyVideo, data=serializer_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
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
    
    serializer = VideoModelSerializer(data=video, context={'req': req})
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
        , context={'req': req})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
def likeVideo(req, url):
    return manageLikes(req, url, 'like')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
def dislikeVideo(req, url):
    return manageLikes(req, url, 'dislike')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
def unlikeVideo(req, url):
    return manageLikes(req, url, 'unlike')

def manageLikes(req, url, method):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    getattr(video, method)(req.user)
    serializer = VideoModelSerializer(video, context={'req': req})
    return Response(serializer.data, status=status.HTTP_200_OK)