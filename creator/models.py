from django.db import models

from authC.models import User

class Creator(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField("first name", max_length=255)
    last_name = models.CharField("last name", max_length=255, blank=True, null=True)
    contacts = models.TextField("contacts", blank=True, null=True)
    description = models.TextField("description", blank=True, null=True)
    channel_background = models.CharField("channel background", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.first_name


