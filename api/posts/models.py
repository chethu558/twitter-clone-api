from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.tweet
    
class Likes(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.tweet

class Comments(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.tweet
    



    
