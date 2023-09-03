import os
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
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ffmpeg import FFmpeg
import MePipe.settings as settings

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
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([VideoJSONRenderer])
@parser_classes([MultiPartParser, FormParser])
def addVideo(req, format="mp4"):
    try:
        creator = Creator.objects.get(user_id = req.user.id)
    except creator.DoesNotExist:
        creator = None
    if not creator:
        return Response({
            value: 'You are not a creator yet',
            status_code: '400',
        }, status=status.HTTP_400_BAD_REQUEST)
    print(req.data['video'])
    print(default_storage.save('2.mp45', ContentFile(req.data['video'].read())))
    # file = codecs.decode(req.data['video'].read(), encoding='utf-32-be').encode('utf-8')
    # print(type(file.file.getbuffer()))
    
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(os.path.join(settings.MEDIA_ROOT, '2.mp45'))
        .output(
            os.path.join(settings.MEDIA_ROOT, 'test.mp4'),
            codec="copy",
            format="mp4",
        )
    )
    ffmpeg.execute()

    # with open('C:\\Users\\oldi\\Documents\\123\\out.mp4','w') as f:
    #     f.write(out)

    return Response({}, status=status.HTTP_201_CREATED)
    # creator = req.data.get('video', {})
    # creator['user_id'] = req.user.id
    # serializer = CreatorModelSerializer(data=creator)
    # serializer.is_valid(raise_exception=True)
    # serializer.save()
    # return Response(serializer.data, status=status.HTTP_201_CREATED)
    