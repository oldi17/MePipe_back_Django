from django.urls import path

from .views import getCreatorWithUsername, registerCreator, modifyCreator, removeCreator, getCreatorById, getCreatorByName, subscribeToCreator, unsubscribeToCreator, getMe

app_name = 'creator'

urlpatterns = [
    path('reg/', registerCreator, name='register'),
    path('modify/', modifyCreator, name='modify'),
    path('del/', removeCreator, name='modify'),
    path('get/<str:name>', getCreatorByName, name='get'),
    path('get/id/<str:id>', getCreatorById, name='get'),
    path('getMe/', getMe, name='getMe'),
    path('sub/<str:name>', subscribeToCreator, name='sub'),
    path('unsub/<str:name>', unsubscribeToCreator, name='unsub'),
    path('username/<str:name>', getCreatorWithUsername, name='get username')
]