from .models import Comment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class CommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ()
    
    def create(self, validated_data):
        if len(validated_data['content']) == 0:
            raise ValidationError(detail='content must be 1 char or more')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.modified = True
        if not validated_data.get('content', None):
            raise ValidationError(detail='content is required')

        if len(validated_data['content']) == 0:
            raise ValidationError(detail='content must be 1 char or more')
        instance.content = validated_data['content']

        validated_data['modified'] = True
        return super().update(instance, validated_data)