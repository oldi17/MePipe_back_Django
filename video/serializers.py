from math import ceil
import os
from rest_framework import serializers
from rest_framework.exceptions import UnsupportedMediaType
from django.core.exceptions import SuspiciousFileOperation
from authC.models import User
from django.core.files.base import ContentFile
from creator.models import Creator


from video.utils import getMediaInfo, saveImage16x9, saveVideo16x9

from .models import HistoryVideo, Video
import MePipe.settings as settings

class VideoModelSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    thumbnail = serializers.ImageField(write_only=True)

    class Meta:
        model = Video
        exclude = ()

    def create(self, validated_data):
        imgData = getMediaInfo(validated_data['thumbnail'].read())
        if not imgData.get('format_name', None) in ('png_pipe', 'jpeg_pipe', 'webp_pipe',):
            raise UnsupportedMediaType('', detail='Loaded thumbnail is not valid (supported formats: png, jpeg, webp)')

        videoData = getMediaInfo(validated_data['file'].read())
        if not videoData.get('duration', None):
            raise UnsupportedMediaType('', detail='Loaded file is not valid video')
        
        duration = ceil(float(videoData.get('duration')))
        
        try:
            saveImage16x9(validated_data['thumbnail'].file, 
                          os.path.join(settings.MEDIA_ROOT_THUMB, validated_data['url'] + '.jpg'))
            saveVideo16x9(validated_data['file'].file, 
                          videoData.get('format_name'),
                          os.path.join(settings.MEDIA_ROOT_VIDEO, validated_data['url'] + '.mp4'))
            
        except:
            raise SuspiciousFileOperation
        
        validated_data['duration'] = duration
        validated_data.pop('file')
        validated_data.pop('thumbnail')

        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        thumbnail = validated_data.pop('thumbnail', None)
        if thumbnail:
            imgData = getMediaInfo(thumbnail.read())
            if not imgData.get('format_name', None) in ('png_pipe', 'jpeg_pipe', 'webp_pipe',):
                raise UnsupportedMediaType('', detail='Loaded thumbnail is not of supported format(png, jpeg, webp)')
            
            saveImage16x9(thumbnail.file, 
                          os.path.join(settings.MEDIA_ROOT_THUMB, instance.url + '.jpg'))
        
        title = validated_data.pop('title', None)
        if title:
            setattr(instance, 'title', title)
        
        description = validated_data.pop('description', None)
        if description:
            setattr(instance, 'description', description)
        
        instance.save()
        return instance
    
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['likes'] = instance.getLikesNumber()
        ret['dislikes'] = instance.getDislikesNumber()
        ret['creator_name'] = Creator.objects.get(id = instance.creator_id.id).name
        req = self.context.get("req")
        url = self.context.get("url")
        if req and isinstance(req.user, User):
            user = req.user
            ret['isliked'] = instance.isLikedByUser(user)
        return ret

class HistoryVideoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryVideo
        exclude = ()
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        time = validated_data.pop('time', 0)
        setattr(instance, 'time', time)
        instance.save()
        return instance
