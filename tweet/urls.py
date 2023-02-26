from django.urls import path
from .views import TweetCreate, MyTweetList, MyTweetListOldest, TweetFriendList, TweetDetail, TweetFriendListOldest, TweetUserList

urlpatterns = [
    path('', TweetCreate.as_view()),
    path('list/', MyTweetList.as_view()),
    path('list/oldest/', MyTweetListOldest.as_view()),
    path('friends/', TweetFriendList.as_view()),
    path('friends/oldest/', TweetFriendListOldest.as_view()),
    path('<int:pk>', TweetDetail.as_view()),
    path('search/<int:pk>', TweetUserList.as_view()),
]