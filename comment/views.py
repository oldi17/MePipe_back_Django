from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, 
    permission_classes,
    renderer_classes,
    )
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, PermissionDenied


from .models import Comment
from video.models import Video
from .renderers import CommentJSONRenderer
from .serializers import CommentModelSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def getComments(req, url):
    comments = Comment.objects.filter(video_url = url)
    resp = []
    for comment in comments:
        resp.push(CommentModelSerializer(comment).data)
    return Response({'comments': resp}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def addComment(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    
    comment = req.data.get('comment', None)
    comment['user_id'] = video.id
    comment['video_url'] = video.url
    
    serializer = CommentModelSerializer(data=comment)
    serializer.is_valid(raise_exception=True)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def modifyComment(req):
    serializer_data = req.data.get('comment', None)

    try:
        comment = Comment.objects.get(id = serializer_data.get('id', None))
    except:
        raise NotFound('No such comment')
    
    if comment.user_id != req.user:
        raise PermissionDenied('It\'s not your comment')

    serializer = CommentModelSerializer(
        comment, data=serializer_data, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def likeComment(req, id):
    comment = checkComment(req, id)
    comment.like(req.user)
    serializer = CommentModelSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def dislikeComment(req, id):
    comment = checkComment(req, id)
    comment.dislike(req.user)
    serializer = CommentModelSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def unlikeComment(req, id):
    comment = checkComment(req, id)
    comment.unlike(req.user)
    serializer = CommentModelSerializer(comment)
    return Response(serializer.data, status=status.HTTP_200_OK)

def checkComment(req, id):
    try:
        comment = Comment.objects.get(id = id)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    
    if comment.user_id != req.id:
        raise PermissionDenied('It\'s not your comment')
    
    return comment