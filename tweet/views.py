from rest_framework.views import APIView
from .models import Tweet
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework import permissions, status
from users.serializers import UserSerializer
from django.db.models import Q
from django.contrib.auth import get_user_model

class TweetCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        user_info = UserSerializer(request.user)
        close_friends = request.data.get('close_friends')
        if close_friends is None or len(close_friends) == 0:
            close_friends = []
        else:
            close_friends = [int(id_str) for id_str in close_friends.split(",")]
            
        serializer = TweetSerializer(
            data = {
                'user': request.user.id,
                'author': user_info.data['username'],
                'profile_picture': user_info.data['photo_profile'],
                'content': request.data["content"],
                'is_public' : request.data["is_public"],
                'close_friends': close_friends,
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': "Create success",
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MyTweetList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        tweets = Tweet.objects.filter(user = request.user).order_by('-publish_date')
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)

class MyTweetListOldest(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        tweets = Tweet.objects.filter(user = request.user).order_by('publish_date')
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    
class TweetFriendList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        tweets = Tweet.objects.filter( Q(close_friends = request.user.id) | Q(user = request.user) | Q(is_public = True)).order_by('-publish_date')
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    
class TweetFriendListOldest(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        tweets = Tweet.objects.filter( Q(close_friends = request.user.id) | Q(user = request.user) | Q(is_public = True)).order_by('publish_date')
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data)
    
class TweetUserList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, pk):
        try :
            user_found = get_user_model().objects.get(id=pk)
            tweets = Tweet.objects.filter( Q(user=user_found, is_public=True) |
    Q(user=user_found, is_public=False, close_friends = request.user.id)).order_by('-publish_date')
            serializer = TweetSerializer(tweets, many=True)
            return Response(serializer.data)
        except :
            return Response({
                'error' : 'User does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
    
class TweetDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        try : 
            tweets = Tweet.objects.get(pk=pk)
            serializer = TweetSerializer(tweets)
            return Response(serializer.data)
        except :
            return Response({
                'error' : 'Tweet does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk):
        try :
            tweets = Tweet.objects.get(pk=pk)
            close_friends = request.data.get('close_friends')
            if close_friends is None or len(close_friends) == 0:
                close_friends = []
            else:
                close_friends = [int(id_str) for id_str in close_friends.split(",")]

            serializer = TweetSerializer(tweets, data = {
                'content': request.data["content"],
                'is_public' : request.data["is_public"],
                'close_friends': close_friends,
            }, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': "Update success",
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({
                'error' : 'Tweet does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        try :
            tweets = Tweet.objects.get(pk=pk)
            tweets.delete()
            return Response({
                'status': 'Deleted',
            }, status=status.HTTP_201_CREATED)
        except :
            return Response({
                'error' : 'Tweet does not exist'
            }, status=status.HTTP_404_NOT_FOUND)