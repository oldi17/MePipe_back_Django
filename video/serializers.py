from rest_framework import serializers

from .models import Video

class VideoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ( )
    
    def create(self, validated_data):
        video = super().create(validated_data)
        return video
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance