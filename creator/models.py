from django.db import models

from authC.models import User

class Creator(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    contacts = models.TextField(blank=True)
    description = models.TextField(blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers', blank=True)

    def __str__(self):
        return self.name

    def getSubscribersNumber(self):
        return self.subscribers.count()
    
    def subscribe(self, user:User):
        self.subscribers.add(user)

    def unsubscribe(self, user:User):
        self.subscribers.remove(user)
    
    def isSubscribedByUser(self, user:User):
        if self.subscribers.contains(user):
            return True
        return False