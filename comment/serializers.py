from .models import Comment
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from authC.models import User

class CommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ()
    
    def create(self, validated_data):
        if len(validated_data['content']) == 0:
            raise ValidationError(detail='content must be 1 char or more')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validated_data.get('content', None):
            raise ValidationError(detail='content is required')

        if len(validated_data['content']) == 0:
            raise ValidationError(detail='content must be 1 char or more')
        
        instance.content = validated_data['content']
        instance.modified = True
        instance.save()
        return instance
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['likes'] = instance.getLikesNumber()
        ret['dislikes'] = instance.getDislikesNumber()
        ret['user_username'] = User.objects.get(id = instance.user_id.id).username

        req = self.context.get("req")
        if req and isinstance(req.user, User):
            user = req.user
            ret['isliked'] = instance.isLikedByUser(user)
        
        return ret