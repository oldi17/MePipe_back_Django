from rest_framework import serializers

from .models import Creator

class CreatorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        exclude = ('id', )
    
    def create(self, validated_data):
        creator = super().create(validated_data)
        return creator
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance