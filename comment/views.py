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
from django.db.models import Count


from .models import Comment
from video.models import Video
from .renderers import CommentJSONRenderer
from .serializers import CommentModelSerializer
from MePipe.utils import paginate


@api_view(['GET'])
@permission_classes([AllowAny])
def getComments(req, url):
    comments = Comment.objects \
        .filter(video_url = url) \
        .annotate(likes_count = Count('likes')) \
        .order_by('-likes_count', '-id')
    return paginate(comments, req, CommentModelSerializer, 'comments')

@api_view(['GET'])
@permission_classes([AllowAny])
def getCommentsCount(req, url):
    comments = Comment.objects \
        .filter(video_url = url)
    return Response(comments.count(), status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def addComment(req, url):
    try:
        video = Video.objects.get(url = url)
    except ObjectDoesNotExist as err:
        raise NotFound('No such video')
    
    comment = req.data.get('comment', None)
    comment['user_username'] = req.user.username
    comment['video_url'] = video.url
    
    serializer = CommentModelSerializer(data=comment, context={'req': req})
    serializer.is_valid(raise_exception=True)
    
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def modifyComment(req, id):
    serializer_data = req.data.get('comment', None)
    comment = getCommentById(id)
    
    if comment.user_username != req.user:
        raise PermissionDenied('It\'s not your comment')

    serializer = CommentModelSerializer(
        comment, data=serializer_data, partial=True, 
        context={'req': req})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def likeComment(req, id):
    return checkComment(req, id, 'like')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def dislikeComment(req, id):
    return checkComment(req, id, 'dislike')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@renderer_classes([CommentJSONRenderer])
def unlikeComment(req, id):
    return checkComment(req, id, 'unlike')

def checkComment(req, id, method):
    comment = getCommentById(id)
    getattr(comment, method)(req.user)
    serializer = CommentModelSerializer(comment, context={'req': req})
    return Response(serializer.data, status=status.HTTP_200_OK)

def getCommentById(id):
    try:
        comment = Comment.objects.get(id = id)
    except ObjectDoesNotExist as err:
        raise NotFound('No such comment')
    return comment