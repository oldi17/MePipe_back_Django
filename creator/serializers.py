import os
from rest_framework import serializers
from rest_framework.exceptions import UnsupportedMediaType

from authC.models import User

from .models import Creator
from .utils import cropAndSaveImage6x1
import MePipe.settings as settings

class CreatorModelSerializer(serializers.ModelSerializer):
    channel_background = serializers.ImageField(write_only=True)

    class Meta:
        model = Creator
        exclude = ()
    
    def create(self, validated_data):
        image = validated_data.pop('channel_background')
        try:
            cropAndSaveImage6x1(image.file, 
                          os.path.join(settings.MEDIA_ROOT_CBG, validated_data['name'] + '.jpg'))
        except:
            raise UnsupportedMediaType('', detail='Loaded thumbnail is not valid (supported formats: png, jpeg, webp)')
        creator = super().create(validated_data)
        return creator
    
    def update(self, instance, validated_data):
        image = validated_data.pop('channel_background', None)
        if image:
            try:
                cropAndSaveImage6x1(image.file, 
                            os.path.join(settings.MEDIA_ROOT_CBG, validated_data['name'] + '.jpg'))
            except:
                raise UnsupportedMediaType('', detail='Loaded thumbnail is not valid (supported formats: png, jpeg, webp)')
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['subscribers'] = instance.getSubscribersNumber()
        ret.pop('user_id')
        req = self.context.get("req")
        if req and isinstance(req.user, User):
            user = req.user
            ret['issubscribed'] = instance.isSubscribedByUser(user)
        
        return ret