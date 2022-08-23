from django.db import models
from email.utils import parsedate_to_datetime

class Message(models.Model):
    user_id = models.CharField(max_length=38)
    party_id = models.CharField(max_length=38)
    message = models.CharField(max_length=280)
    time_sent = models.DateTimeField()

    def __str__():
        return self.user_id + " " + self.party_id + " " + self.message

class Party(models.Model):
    party_id = models.CharField(max_length=38, primary_key=True)
    video_id = models.CharField(max_length=30, default="")
    status = models.BooleanField(default=False)

    def __str__():
        return self.party_id
    
class User(models.Model):
    user_id = models.CharField(max_length=38,primary_key=True)
    username = models.CharField(max_length=255)
    party_id = models.CharField(max_length=38)

    def __str__():
        return self.user_id + " " + self.username + " " + self.party_id