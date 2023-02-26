from django.db import models
from users.models import MyUser

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    author = models.CharField(max_length=100)
    profile_picture = models.URLField(null=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    close_friends = models.ManyToManyField(MyUser, related_name='close_friends', null= True, blank= True)