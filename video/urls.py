from django.urls import path

from .views import dislikeVideo, getVideo, addVideo, likeVideo, modifyVideo, unlikeVideo

app_name = 'video'

urlpatterns = [
    path('add/', addVideo, name='add'),
    path('modify/<str:url>', modifyVideo, name='modify'),
    path('watch/<str:url>', getVideo, name='get'),
    path('like/<str:url>', likeVideo, name='like'),
    path('dislike/<str:url>', dislikeVideo, name='dislike'),
    path('unlike/<str:url>', unlikeVideo, name='unlike'),
]