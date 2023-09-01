from django.urls import path, include

from .views import registerCreator, modifyCreator, getCreator

app_name = 'authC'

creatorURLs = [
    path('reg/', registerCreator, name='register'),
    path('modify/', modifyCreator, name='modify'),
    path('get/<str:username>', getCreator, name='get'),
]

urlpatterns = [
    path('creator/', include(creatorURLs))
]