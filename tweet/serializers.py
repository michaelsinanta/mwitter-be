from rest_framework import serializers
from .models import Tweet
from users.models import MyUser

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'