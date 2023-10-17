import os
from rest_framework import serializers
from rest_framework.exceptions import UnsupportedMediaType

from authC.models import User
from authC.utils import saveImage1x1

from .models import Creator
from .utils import cropAndSaveImage6x1, renameCreator
import MePipe.settings as settings

class CreatorModelSerializer(serializers.ModelSerializer):
    channel_pfp = serializers.ImageField(write_only=True)
    channel_background = serializers.ImageField(write_only=True)

    class Meta:
        model = Creator
        exclude = ()
    
    def create(self, validated_data):
        image = validated_data.pop('channel_background')
        pfp = validated_data.pop('channel_pfp')
        try:
            cropAndSaveImage6x1(image.file, 
                          os.path.join(settings.MEDIA_ROOT_CBG, validated_data['name'] + '.jpg'))
            saveImage1x1(pfp.file,
                          os.path.join(settings.MEDIA_ROOT_CPFP, validated_data['name'] + '.png'))
        except:
            raise UnsupportedMediaType('', detail='Loaded thumbnail is not valid (supported formats: png, jpeg, webp)')
        creator = super().create(validated_data)
        return creator
    
    def update(self, instance, validated_data):
        image = validated_data.pop('channel_background', None)
        pfp = validated_data.pop('channel_pfp', None)
        if image:
            try:
                cropAndSaveImage6x1(image.file, 
                            os.path.join(settings.MEDIA_ROOT_CBG, instance.name + '.jpg'))
            except:
                raise UnsupportedMediaType('', detail='Loaded thumbnail is not valid (supported formats: png, jpeg, webp)')
        if pfp:
            try:
                saveImage1x1(pfp.file,
                          os.path.join(settings.MEDIA_ROOT_CPFP, instance.name + '.png'))
            except:
                raise UnsupportedMediaType('', detail='Loaded profile picture is not valid (supported formats: png, jpeg, webp)')
        
        oldName = instance.name
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        renameCreator(oldName, instance.name)

        return instance
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subscribers'] = instance.getSubscribersNumber()
        req = self.context.get("req")
        if req and isinstance(req.user, User):
            user = req.user
            ret['issubscribed'] = instance.isSubscribedByUser(user)
        
        return ret