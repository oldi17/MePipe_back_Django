from django.urls import path

from .views import (
    delHistoryVideo, getRecVideo, getSubVideos, getVideo, addVideo, modifyVideo,
    dislikeVideo, likeVideo, unlikeVideo,
    getHistoryVideo, setHistoryVideoTime,
    getCreatorVideo, getAllVideo, getAllHistoryVideo,
    delVideo, getSearchVideo)

app_name = 'video'

urlpatterns = [
    path('add/', addVideo, name='add'),
    path('modify/<str:url>', modifyVideo, name='modify'),
    path('watch/<str:url>', getVideo, name='get'),
    path('like/<str:url>', likeVideo, name='like'),
    path('dislike/<str:url>', dislikeVideo, name='dislike'),
    path('unlike/<str:url>', unlikeVideo, name='unlike'),
    path('del/<str:url>', delVideo, name='unlike'),

    path('creator/<str:name>', getCreatorVideo, name='get creator'),
    path('all/', getAllVideo, name='get all'),
    path('rec/all/<str:name>', getRecVideo, name='get all recomended'),
    path('sub/all/', getSubVideos, name='get all sub videos'),
    
    path('search/', getSearchVideo, name='get all sub videos'),
    
    path('history/all/', getAllHistoryVideo, name='get all history'),
    path('history/t/<str:url>', setHistoryVideoTime, name='set time of history video'),
    path('history/watch/<str:url>', getHistoryVideo, name='get history video'),
    path('history/del/<str:url>', delHistoryVideo, name='delete history video'),

]