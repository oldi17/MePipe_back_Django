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
from authC.models import User
from django.db.models.expressions import Case, When
from django.db.models import Q
import operator
from functools import reduce

from creator.models import Creator
from video.utils import generateURL, removeVideoFiles
from .models import Video, HistoryVideo
from .renderers import HistoryVideoJSONRenderer, VideoJSONRenderer
from .serializers import VideoModelSerializer, HistoryVideoModelSerializer
from MePipe.utils import paginate

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllHistoryVideo(req):
    historyVideos = HistoryVideo.objects \
        .filter(user_id = req.user.id) \
        .select_related('video_url') \
        .order_by('-watchedAt')
    videos = [hv.video_url for hv in historyVideos]
    return paginate(videos, req, VideoModelSerializer, 'videos')

@api_view(['GET'])
@permission_classes([AllowAny])
def getCreatorVideo(req, name):
    video = Video.objects \
        .filter(creator_id = getCreatorIdByName(name)) \
        .order_by('-id')
    return paginate(video, req, VideoModelSerializer, 'videos')

@api_view(['GET'])
@permission_classes([AllowAny])
def getAllVideo(req):
    video = Video.objects.all().order_by('-id')
    return paginate(video, req, VideoModelSerializer, 'videos', 15)

@api_view(['POST'])
@permission_classes([AllowAny])
def getSearchVideo(req):
    query = req.data.get('query', '')
    reducedTitle = reduce(operator.and_, (Q(title__icontains=x) for x in query.split(' ')))
    reducedDescription = reduce(operator.and_, (Q(description__icontains=x) for x in query.split(' ')))
    video = Video.objects \
        .filter(reducedTitle | reducedDescription).order_by('-id')
    return paginate(video, req, VideoModelSerializer, 'videos')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSubVideos(req):
    creators = Creator.objects.filter(subscribers__in = [req.user])
    video = Video.objects.filter(creator_id__in = creators).order_by('-id')
    return paginate(video, req, VideoModelSerializer, 'videos')

@api_view(['GET'])
@permission_classes([AllowAny])
def getRecVideo(req, name):
    videos = Video.objects.all() \
        .annotate(is_creator_video = Case(When(creator_id = getCreatorIdByName(name), then=1), default=0)) \
        .order_by('-is_creator_video', '-id')
    return paginate(videos, req, VideoModelSerializer, 'videos')

@api_view(['GET'])
@permission_classes([AllowAny])
@renderer_classes([VideoJSONRenderer])
def getVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')

    serializer = VideoModelSerializer(video, context={'req': req, 'url': url})
    res = serializer.data

    if isinstance(req.user, User):
        historyVideo = HistoryVideo.objects.filter(user_id = req.user.id, video_url=video.url).first()
        if historyVideo:
            res['timestamp'] = historyVideo.time
        else:
            hisSerializer = HistoryVideoModelSerializer(data={
                'user_id': req.user.id, 
                'video_url': video.url
            })
            hisSerializer.is_valid(raise_exception=True)
            hisSerializer.save()
            res['timestamp'] = 0
            
    video.addView()
    
    return Response(res, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([HistoryVideoJSONRenderer])
def getHistoryVideo(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    try:
        historyVideo = HistoryVideo.objects.get(video_url = url, user_id = req.user)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video in history')
    serializer = HistoryVideoModelSerializer(historyVideo)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delHistoryVideo(req, url):
    try:
        historyVideo = HistoryVideo.objects.get(video_url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video in history')
    historyVideo.delete()
    return Response('removed', status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([HistoryVideoJSONRenderer])
def setHistoryVideoTime(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    try:
        historyVideo = HistoryVideo.objects.get(video_url = video.url, user_id = req.user)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video in history')
    serializer = HistoryVideoModelSerializer(historyVideo, data=req.data, partial=True)
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
  
    video = req.data.dict()
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delVideo(req, url):
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
    
    try:
        url = video.url
        video.delete()
        removeVideoFiles(url)
    except Exception as ex:
        return Response('Something went wrong', status=status.HTTP_409_CONFLICT)
    return Response('removed', status=status.HTTP_200_OK)

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

def getCreatorIdByName(name):
    return Creator.objects.get(name = name).id