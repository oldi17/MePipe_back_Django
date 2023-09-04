from django.urls import path

from .views import getVideo, addVideo

app_name = 'video'

urlpatterns = [
    path('add/', addVideo, name='add'),
    # path('modify/', modifyCreator, name='modify'),
    path('watch/<str:url>', getVideo, name='get'),
]