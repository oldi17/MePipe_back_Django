from django.db import models

from authC.models import User
from video.models import Video

class Comment(models.Model):
    user_username = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    video_url = models.ForeignKey(Video, on_delete=models.CASCADE, to_field='url')
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modified = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='clikes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='cdislikes', blank=True)

    def like(self, user:User):
        self.likes.add(user)
        self.dislikes.remove(user)
    
    def dislike(self, user:User):
        self.dislikes.add(user)
        self.likes.remove(user)
    
    def unlike(self, user:User):
        self.dislikes.remove(user)
        self.likes.remove(user)

    def getLikesNumber(self):
        return self.likes.count()
    
    def getDislikesNumber(self):
        return self.dislikes.count()
    
    def isLikedByUser(self, user:User):
        if  self.likes.contains(user):
            return 1
        elif self.dislikes.contains(user):
            return -1
        return 0