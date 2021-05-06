from django.contrib import admin
from django.urls import path,include

from rest_framework.routers import DefaultRouter

#import views
from .import views

router = DefaultRouter()
#router.register(r'', views.UserViewSet)

urlpatterns = [
    path('tweet/', views.Tweets.as_view(), name="tweet"),
    path('like/', views.like_dislike, name="like-dislike"),
    path('comment/', views.Comment.as_view(), name="comment"),
    path('likes/<int:tweet_id>/', views.total_likes, name="likes"),
    path('comments/<int:tweet_id>/', views.total_comments, name="comments"),
]