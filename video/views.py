from datetime import datetime
import json
from math import ceil
import os
import subprocess
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    parser_classes
    )
from django.core.exceptions import ObjectDoesNotExist, SuspiciousFileOperation
from rest_framework.exceptions import NotFound, PermissionDenied, UnsupportedMediaType
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import MePipe.settings as settings
import codecs
from PIL import Image

from creator.models import Creator
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
    except creator.DoesNotExist:
        creator = None
    if not creator:
        raise PermissionDenied('You are not a creator yet')
    
    video = req.data
    file = video['file'].read()
    thumbnail = video['thumbnail'].file

    link = str(hash(str(datetime.now()) + settings.SECRET_KEY))
    enc = codecs.encode(link.encode(), 'base64')[:-1].decode("utf-8")

    video['creator_id'] = creator.id
    video['url'] = enc
    serializer = VideoModelSerializer(data=video)
    serializer.is_valid(raise_exception=True)

    try:
        imgData = json.loads(probe_file(thumbnail.read())[0]).get('format', {})
        if not imgData.get('format_name', None) in ('png_pipe', 'jpeg_pipe', 'webp_pipe',):
            raise UnsupportedMediaType('', detail='Loaded thumbnail is not of supported format(png, jpeg, webp)')

        im = Image.open(thumbnail)
        im = im.convert('RGB')
        im = make_16x9(im)
        im.save(os.path.join(settings.MEDIA_ROOT_THUMB, enc + '.jpg'))

        path = os.path.join(settings.MEDIA_ROOT_VIDEO, enc + '.mp4')

        videoData = json.loads(probe_file(file)[0]).get('format', {})   
        if not videoData.get('duration', None):
            raise UnsupportedMediaType('', detail='Loaded file is not a video')
        
        serializer.validated_data['duration'] = ceil(float(videoData.get('duration')))

        if 'mp4' in videoData.get('format_name'):
            default_storage.save(path, ContentFile(file))
        else:
            convert_file(file, path)
    except:
        raise SuspiciousFileOperation
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

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

def probe_file(pipe):
    cmnd = [settings.FFPROBE_PATH, '-v', 'quiet', '-print_format', 'json', '-show_format', 'pipe:0']
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(input=pipe)
    return out, err

def convert_file(pipe, outFileName):
    outFileName = outFileName.replace('\\', '/')
    cmnd = [settings.FFMPEG_PATH, 
            '-i', 'pipe:0',
            '-c:v', 'libx264',
            '-c:a', 'copy',
            '-y',
            '' + outFileName + '',
            ]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate(input=pipe)
    return out, err

def make_16x9(im, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = int(max(x / 16, y / 9))
    new_im = Image.new('RGB', (size * 16, size * 9), fill_color)
    new_im.paste(im, (int((size * 16 - x) / 2), int((size * 9 - y) / 2)))
    return new_im