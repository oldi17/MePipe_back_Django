from django.urls import path

from .views import (dislikeComment, getCommentsCount, getComments, 
                    addComment, likeComment, modifyComment, 
                    unlikeComment, removeComment)

app_name = 'comment'

urlpatterns = [
    path('add/<str:url>', addComment, name='add'),
    path('modify/<int:id>', modifyComment, name='modify'),
    path('del/<int:id>', removeComment, name='remove'),
    path('all/<str:url>', getComments, name='get'),
    path('count/<str:url>', getCommentsCount, name='get'),
    path('like/<int:id>', likeComment, name='like'),
    path('dislike/<int:id>', dislikeComment, name='dislike'),
    path('unlike/<int:id>', unlikeComment, name='unlike'),
]