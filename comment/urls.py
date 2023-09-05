from django.urls import path

from .views import dislikeComment, getComments, addComment, likeComment, modifyComment, unlikeComment

app_name = 'comment'

urlpatterns = [
    path('add/<str:url>', addComment, name='add'),
    path('modify/<int:id>', modifyComment, name='modify'),
    path('all/<str:url>', getComments, name='get'),
    path('like/<int:id>', likeComment, name='like'),
    path('dislike/<int:id>', dislikeComment, name='dislike'),
    path('unlike/<int:id>', unlikeComment, name='unlike'),
]