from django.urls import path

from .views import registerCreator, modifyCreator, getCreator, subscribeToCreator, unsubscribeToCreator, getMe

app_name = 'creator'

urlpatterns = [
    path('reg/', registerCreator, name='register'),
    path('modify/', modifyCreator, name='modify'),
    path('get/<str:name>', getCreator, name='get'),
    path('getMe/', getMe, name='getMe'),
    path('sub/<str:name>', subscribeToCreator, name='sub'),
    path('unsub/<str:name>', unsubscribeToCreator, name='unsub'),
]