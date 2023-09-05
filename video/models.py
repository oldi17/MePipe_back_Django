from django.db import models
from functools import reduce

from creator.models import Creator
from authC.models import User

class Video(models.Model):
    creator_id = models.ForeignKey(Creator, on_delete=models.CASCADE)
    title = models.CharField("title", max_length=255)
    description = models.TextField("description", blank=True, null=True)
    url = models.CharField("url", max_length=255, unique=True)
    duration = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)

    def __str__(self):
        return self.url
    
    def getLikesNumber(self):
        return self.likes.count()
    
    def getDislikesNumber(self):
        return self.dislikes.count()
    
    def like(self, user:User):
        self.likes.add(user)
        self.dislikes.remove(user)
    
    def dislike(self, user:User):
        self.dislikes.add(user)
        self.likes.remove(user)
    
    def unlike(self, user:User):
        self.dislikes.remove(user)
        self.likes.remove(user)
    
    def addView(self):
        self.views += 1
        self.save()
    
    def isLikedByUser(self, user:User):
        if user in self.likes:
            return 1
        elif user in self.dislikes:
            return -1
        return 0